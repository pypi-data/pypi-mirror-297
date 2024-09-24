import re
import sys

from OpenSSL import crypto

from pandaserver.taskbuffer import JobUtils


# get prefix for DQ2
def getDQ2Prefix(dq2SiteID):
    try:
        # prefix of DQ2 ID
        tmpDQ2IDPrefix = re.sub("_[A-Z,0-9]+DISK$", "", dq2SiteID)
        # remove whitespace
        tmpDQ2IDPrefix = tmpDQ2IDPrefix.strip()
        # patchfor MWT2
        if tmpDQ2IDPrefix == "MWT2_UC":
            tmpDQ2IDPrefix = "MWT2"
        return tmpDQ2IDPrefix
    except Exception:
        return ""


# check if the file is cached
def isCachedFile(datasetName, siteSpec):
    # using CVMFS
    if siteSpec.iscvmfs is not True:
        return False
    # look for DBR
    if not datasetName.startswith("ddo"):
        return False
    # look for three digits
    if re.search("v\d{6}$", datasetName) is None:
        return False
    return True


# get the list of sites where dataset is available
def get_endpoints_at_nucleus(tmpRepMap, siteMapper, cloudName):
    """
    Retrieves a list of DDM endpoints at the nucleus for a given cloud.

    Returns:
        list: A list of DDM endpoints that are part of the nucleus for the specified cloud. This list includes
              only those endpoints that have replicas of the datasets in `tmpRepMap`.
    """
    retList = []
    # get cloud SEs
    tmpCloud = siteMapper.getCloud(cloudName)
    cloudSEs = tmpCloud["tier1SE"]
    # check Nucleus endpoints
    for tmpSePat in cloudSEs:
        # ignore empty
        if tmpSePat == "":
            continue
        # make regexp pattern
        if "*" in tmpSePat:
            tmpSePat = tmpSePat.replace("*", ".*")
        tmpSePat = "^" + tmpSePat + "$"
        # loop over all sites
        for tmpSE in tmpRepMap:
            # check match
            if re.search(tmpSePat, tmpSE) is None:
                continue
            # append
            if tmpSE not in retList:
                retList.append(tmpSE)
    # return
    return retList


# check if the dataset is a DB release
def isDBR(datasetName):
    if datasetName.startswith("ddo"):
        return True
    return False


# check invalid characters in dataset name
def checkInvalidCharacters(datasetName):
    if re.match("^[A-Za-z0-9][A-Za-z0-9\.\-\_/]{1,255}$", datasetName) is not None:
        return True
    return False


# get dataset type
def getDatasetType(dataset):
    datasetType = None
    try:
        datasetType = dataset.split(".")[4]
    except Exception:
        pass
    return datasetType


# get sites which share DDM endpoint
def getSitesShareDDM(siteMapper, siteName, prodSourceLabel, job_label, output_share=False):
    # output_share: False to get sites which use the output RSE as input, True to get sites which use
    #               the input RSEs as output

    # nonexistent site
    if not siteMapper.checkSite(siteName):
        return []
    # get siteSpec
    siteSpec = siteMapper.getSite(siteName)
    scope_site_input, scope_site_output = select_scope(siteSpec, prodSourceLabel, job_label)
    runs_production = siteSpec.runs_production()
    runs_analysis = siteSpec.runs_analysis()
    # loop over all sites
    retSites = []
    for tmpSiteName in siteMapper.siteSpecList:
        tmpSiteSpec = siteMapper.siteSpecList[tmpSiteName]
        scope_tmpSite_input, scope_tmpSite_output = select_scope(tmpSiteSpec, prodSourceLabel, job_label)
        # only same type
        if (runs_production and not tmpSiteSpec.runs_production()) or (runs_analysis and not tmpSiteSpec.runs_analysis()):
            continue
        # only online sites
        if tmpSiteSpec.status != "online":
            continue
        # same endpoint
        try:
            if not output_share and siteSpec.ddm_output[scope_site_output] not in tmpSiteSpec.ddm_endpoints_input[scope_tmpSite_input].all:
                continue
            if output_share and tmpSiteSpec.ddm_output[scope_site_output] not in siteSpec.ddm_endpoints_input[scope_tmpSite_input].all:
                continue
        except Exception:
            continue
        # skip itself
        if siteName == tmpSiteSpec.sitename:
            continue
        # append
        if tmpSiteSpec.sitename not in retSites:
            retSites.append(tmpSiteSpec.sitename)
    # return
    return retSites


# check if destination is specified
def getDestinationSE(destinationDBlockToken):
    if destinationDBlockToken is not None:
        for tmpToken in destinationDBlockToken.split(","):
            tmpMatch = re.search("^dst:([^/]*)(/.*)*$", tmpToken)
            if tmpMatch is not None:
                return tmpMatch.group(1)
    return None


# check if job sets destination
def checkJobDestinationSE(tmpJob):
    for tmpFile in tmpJob.Files:
        if getDestinationSE(tmpFile.destinationDBlockToken) is not None:
            return tmpFile.destinationSE
    return None


# check if destination is distributed
def getDistributedDestination(destinationDBlockToken, ignore_empty=True):
    if destinationDBlockToken is not None:
        for tmpToken in destinationDBlockToken.split(","):
            tmpMatch = re.search("^ddd:([^/]*)(/.*)*$", tmpToken)
            if tmpMatch is not None:
                loc = tmpMatch.group(1)
                if ignore_empty and not loc:
                    return None
                return loc
    return None


# extract importand error string
def extractImportantError(out):
    retStr = ""
    try:
        strList = ["InvalidRSEExpression", "Details:"]
        for line in out.split("\n"):
            for tmpStr in strList:
                if tmpStr in line:
                    retStr += line
                    retStr += " "
        retStr = retStr[:-1]
    except Exception:
        pass
    return retStr


# get activity for output
def getActivityForOut(prodSourceLabel):
    if prodSourceLabel in ["managed"]:
        activity = "Production Output"
    elif prodSourceLabel in ["user", "panda"]:
        activity = "Analysis Output"
    else:
        activity = "Functional Test"
    return activity


def select_scope(site_spec, prodsourcelabel, job_label):
    """
    Select the scopes of the activity for input and output. The scope was introduced for prod-analy queues
    where you might want to associate different RSEs depending on production or analysis.
    """
    scope_input = "default"
    aux_scopes_input = site_spec.ddm_endpoints_input.keys()
    if (job_label == JobUtils.ANALY_PS or prodsourcelabel in JobUtils.analy_sources) and "analysis" in aux_scopes_input:
        scope_input = "analysis"

    scope_output = "default"
    aux_scopes_output = site_spec.ddm_endpoints_output.keys()
    if (job_label == JobUtils.ANALY_PS or prodsourcelabel in JobUtils.analy_sources) and "analysis" in aux_scopes_output:
        scope_output = "analysis"

    return scope_input, scope_output


def is_top_level_dataset(dataset_name: str) -> bool:
    """
    Check if top dataset

    Args:
        dataset_name (str): Dataset name.

    Returns:
        bool: True if top dataset, False otherwise.
    """
    return re.sub("_sub\d+$", "", dataset_name) == dataset_name


def is_sub_dataset(dataset_name: str) -> bool:
    """
    Check if the dataset name ends with '_sub' followed by one or more digits.

    Args:
        dataset_name (str): The name of the dataset.

    Returns:
        bool: True if the dataset name ends with '_sub' followed by one or more digits, False otherwise.
    """
    return re.search("_sub\d+$", dataset_name) is not None


def is_tid_dataset(destination_data_block: str) -> bool:
    """
    Check if the destination data block ends with '_tid' followed by one or more digits.

    Args:
        destination_data_block (str): The destination data block.

    Returns:
        bool: True if the destination data block ends with '_tid' followed by one or more digits, False otherwise.
    """
    return re.search("_tid[\d_]+$", destination_data_block) is not None


def is_hammercloud_dataset(destination_data_block: str) -> bool:
    """
    Check if the destination data block starts with 'hc_test.'.

    Args:
        destination_data_block (str): The destination data block.

    Returns:
        bool: True if the destination data block starts with 'hc_test.', False otherwise.
    """
    return re.search("^hc_test\.", destination_data_block) is not None


def is_user_gangarbt_dataset(destination_data_block: str) -> bool:
    """
    Check if the destination data block starts with 'user.gangarbt.'.

    Args:
        destination_data_block (str): The destination data block.

    Returns:
        bool: True if the destination data block starts with 'user.gangarbt.', False otherwise.
    """
    return re.search("^user\.gangarbt\.", destination_data_block) is not None


def is_lib_dataset(destination_data_block: str) -> bool:
    """
    Check if the destination data block ends with '.lib'.

    Args:
        destination_data_block (str): The destination data block.

    Returns:
        bool: True if the destination data block ends with '.lib', False otherwise.
    """
    return re.search("\.lib$", destination_data_block) is not None
