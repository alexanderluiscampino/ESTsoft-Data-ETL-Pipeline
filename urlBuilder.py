def urlBuilder_Billing_statsPeriodOld(sitecode, initialDate, finalDate):
    """
    # This function takes as input the site code, initial date and final date
    and returns the url for the statistic period of interest.
    # @sitecode, initialDate, finalDate
    # @url
    """
    sitecode = "sitecode={}".format(sitecode)
    codes = "chargetype=1&chkmenuid=711&periodtype=1&type=2&cashtype=&usestate=1&cashattr="
    period = "FromYmd={}&ToYmd={}&fromyearmonth=&fromyearmonth2=&toyearmonth=&toyearmonth2=&year=&year2=".format(initialDate, finalDate)
    url = "http://billadmin.cabal.com/Statistics/Graphs/GraphPurchaseData.aspx?{}&{}&{}&gamecode=ALL&allymd=".format(sitecode, codes, period)
    return url
################################################################################
def urlBuilder_Billing_statsPeriod(option):
    if option == 'Revenue':
        return "http://billadmin.cabal.com/Statistics/PurchasePeriodList.aspx?MenuID=711"
    elif option == 'UniquePurchasers':
        return "http://billadmin.cabal.com/UseLog/UseLogList.aspx?MenuID=570"
################################################################################
def urlBuilder_CRM_Login():
    return "http://br.crm.estgames.com:21070/Account/Logon"

def urlBuilder_CRM_MetricCounts(start_date, end_date, metric):
    return "http://br.crm.estgames.com:21070/Sales/UserCount/View?startDate={}&endDate={}&type={}".format(start_date, end_date, metric)
################################################################################
def urlBuilder_CRM_TopItems(start_date, end_date):
    baseURL = "http://br.crm.estgames.com:21070/Sales/Item/GetSum?"
    periodParams = "startDate={}&endDate={}".format(start_date, end_date)

    params = "&type=all&sEcho=1&iColumns=11&sColumns=&iDisplayStart=0&iDisplayLength=1000"

    dataParams = "&mDataProp_0=0" +\
    "&mDataProp_1=1" +\
    "&mDataProp_2=2" +\
    "&mDataProp_3=3" +\
    "&mDataProp_4=4" +\
    "&mDataProp_5=5" +\
    "&mDataProp_6=6" +\
    "&mDataProp_7=7" +\
    "&mDataProp_8=8" +\
    "&mDataProp_9=9" +\
    "&mDataProp_10=10"

    searchParams = "&sSearch=&bRegex=false" +\
    "&sSearch_0=&bRegex_0=false&bSearchable_0=true" +\
    "&sSearch_1=&bRegex_1=false&bSearchable_1=true" +\
    "&sSearch_2=&bRegex_2=false&bSearchable_2=true" +\
    "&sSearch_3=&bRegex_3=false&bSearchable_3=true" +\
    "&sSearch_4=&bRegex_4=false&bSearchable_4=true" +\
    "&sSearch_5=&bRegex_5=false&bSearchable_5=true" +\
    "&sSearch_6=&bRegex_6=false&bSearchable_6=true" +\
    "&sSearch_7=&bRegex_7=false&bSearchable_7=true" +\
    "&sSearch_8=&bRegex_8=false&bSearchable_8=true" +\
    "&sSearch_9=&bRegex_9=false&bSearchable_9=true" +\
    "&sSearch_10=&bRegex_10=false&bSearchable_10=true"

    sortParams = "&iSortCol_0=5&sSortDir_0=desc&iSortingCols=1" +\
    "&bSortable_0=true" +\
    "&bSortable_1=true" +\
    "&bSortable_2=true" +\
    "&bSortable_3=true" +\
    "&bSortable_4=false" +\
    "&bSortable_5=true" +\
    "&bSortable_6=true" +\
    "&bSortable_7=true" +\
    "&bSortable_8=true" +\
    "&bSortable_9=true" +\
    "&bSortable_10=true"

    endParam = "&_=1521163597514"

    return baseURL + periodParams + params + dataParams + searchParams + sortParams + endParam
################################################################################
if __name__ == '__main__':
    print(urlBuilder_CRM_TopItems("20180228","20180306"))
    print(urlBuilder_Billing_statsPeriod('Revenue'))
    print(urlBuilder_CRM_Login())
    print(urlBuilder_CRM_MetricCounts("20180228", "20180306", "DailyNewConnectedAccount"))
