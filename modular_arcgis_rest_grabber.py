try:
    import archook #The module which locates arcgis
    archook.get_arcpy()
    import arcpy
except ImportError:
    raise ImportError("Error in getting arcpy")

import requests,sys,os,random,certifi,time,shutil
arcpy.env.overwriteOutput = True

'''
http://straffa.com/

24.157.37.61:8080(USA) Tested
211.23.19.130:80
209.66.220.124:8080(USA)
103.1.93.50:8080 Nepal
103.16.157.183:8080 Papua NG
115.29.145.48:10086
93.158.212.111:8089 NL Tested


85.185.42.2:8080 IR Tested
'''

##Proxy
proxies = {
    "http": "http://93.158.212.111:8089",
    "https": "http://93.158.212.111:8089",
}

##Agents

AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "Opera/7.50 (Windows XP; U)",
    "Opera/7.50 (Windows ME; U) [en]",
    "Opera/7.51 (Windows NT 5.1; U) [en]",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0",
    "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.2b) Gecko/20021001 Phoenix/0.2",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.23) Gecko/20090825 SeaMonkey/1.1.18",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )",
    "Mozilla/5.0 (Windows; U; ; en-NZ) AppleWebKit/527  (KHTML, like Gecko, Safari/419.3) Arora/0.8.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media Center PC 4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Beamrise/17.2.0.9 Chrome/17.0.939.0 Safari/535.8",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
    "Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0",
    "iTunes/9.0.2 (Windows; N)",
    "Mozilla/5.0 (compatible; Konqueror/4.5; Windows) KHTML/4.5.4 (like Gecko)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; WOW64; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
    "Opera/9.25 (Windows NT 6.0; U; en)",
    "Opera/9.80 (Windows NT 5.2; U; en) Presto/2.2.15 Version/10.10",
    "Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.7.62 Version/11.01",
    "Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0"]

headers = {"User-Agent":random.choice(AGENTS)}
#headers = {"Host": "www.facebook.com","User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cache-Control": "max-age=0"}
## Containers and items
##=========================================================================##
#Variables
















data_location = os.path.split(sys.argv[0])[0]

GDBNAME="Taxpayers"

start_index=50197286
download_feature_count = 100
rest_url= 'XYZ/MapServer/0'
feature_name='T_'


#Merge
merge_feature_count=50
merged_feature_name='FinalTXP'
id_file_name = 'id.txt'
error_file_name = 'error.txt'


wcard_search=feature_name+'*'
flders = ['Error','JSData','Vectors']


#--------------------------------------------------------------------------------------##
current_file =  data_location
link_dir = data_location
urls = []
#Check if the id.txt exists if not then create
def folder_creator(folder_location, folder_name):
    os.chdir(folder_location)
    os.mkdir(folder_name)
    
def gdb_creator(gdb_location, gdb_name):
    arcpy.CreateFileGDB_management(out_folder_path=gdb_location, out_name=gdb_name, out_version="CURRENT")
    
def objectId_downloader(base_url_count, objectId_save_location, id_file_name):
    url_id_count = base_url_count+'/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=true&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'
    url_id_list = base_url_count+'/query?where=1=1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'
    resp_id_count = requests.get(url_id_count).json()
    resp_id_list = requests.get(url_id_list).json()
    id_count = resp_id_count['count']
    id_lst = resp_id_list['objectIds']
    with open(os.path.join(objectId_save_location, id_file_name), 'wb') as idfile:
        idfile.writelines("%s\n" % l for l in id_lst)
        
def json_downloader(base_rest_url, id_range_to_be_downloaded,json_foler_to_save, id_file_name, error_folder_location, error_file_name):
    time.sleep(random.choice([1,2,3,4]))
    cor_url = ','.join(id_range_to_be_downloaded)
    bas_req = str(rest_url)+"/query?where=5=5&text=&objectIds="+cor_url+"&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&f=pjson"
    cafile = certifi.where()
    #r = requests.get(url, verify=cafile)    
    page = requests.get(bas_req,headers = headers,verify=False)#,proxies=proxies, headers = headers
    print page.headers['content-type']
    #print page.headers['User-Agent']
    if (page.status_code == requests.codes.ok):
        name = url[0].replace(",","").replace(" ","")+'.json'
        with open(os.path.join(json_foler_to_save, name), mode='wb') as f:
            f.write(page.text.encode("utf-8"))
        print "Completed:  "+name +"  Completed plus " +str(len(url))
    else:
        name = url[0].replace(",","").replace(" ","")+'.txt'
        with open(os.path.join(error_folder_location, error_file_name), mode='a') as err:
            er = '\n'.join(url).strip()
            err.write(er)
def json_file_path_lister(file_workspace):
    arcpy.env.workspace = file_workspace
    json_file_names_temp = arcpy.ListFiles()
    return [os.path.join(file_workspace,fnt) for fnt in json_file_names_temp]
def feature_class_path_lister(workspace_gdb,wld_card):
    arcpy.env.workspace = workspace_gdb
    feature_class_file_names_temp = arcpy.ListFeatureClasses(wld_card)
    return [os.path.join(workspace_gdb,fnt) for fnt in feature_class_file_names_temp]

def json_to_feature_converter(input_json_path, output_gbd_path, output_featureclass_name):
    output_featureclass_name_temp = os.path.join(output_gbd_path, output_featureclass_name)
    arcpy.JSONToFeatures_conversion(input_json_path,output_featureclass_name_temp)

def feature_merger(list_of_feature_paths_to_merge, output_gdb_location, output_merged_feature_name):
    output_merged_feature_temp = os.path.join(output_gdb_location, output_merged_feature_name)
    arcpy.Merge_management(list_of_feature_paths_to_merge,output_merged_feature_temp)




##RUN
#===================================================================================================
for folder_name_iterator in flders:
    folder_creator(data_location, folder_name_iterator)
gdb_creator(os.path.join(data_location,'Vectors'), GDBNAME)

objectId_downloader(rest_url, data_location, id_file_name)
urls = [line.strip() for line in open(os.path.join(data_location, id_file_name), 'r')]

##Modify list if download obstructed
if start_index:
    start = urls.index(str(start_index))#+901
    urls= urls[start:]
#Download jsons
result = [urls[i:i+download_feature_count] for i in xrange(0, len(urls), download_feature_count)]
for url in result:
    json_downloader(rest_url, url, os.path.join(data_location, 'JSData'),id_file_name, 
                   os.path.join(data_location, 'Error'), error_file_name)

#Convert jsons into feature class
conversion_counter = 1
json_paths = json_file_path_lister(os.path.join(data_location, 'JSData'))
for single_json in json_paths:
    if conversion_counter%50==0:
        print "Completed conversion of %s"%str(conversion_counter)
    feat_name = feature_name+os.path.basename(single_json).split('.')[0]
    json_to_feature_converter(single_json, os.path.join(data_location,'Vectors',GDBNAME+'.gdb'), 
                             feat_name)
    conversion_counter+=1

#Merge featureclass into single one
#------------------------------------------------------------
#Create a temp gdb
arcpy.CreateFileGDB_management(out_folder_path=data_location, out_name='TempMerge', out_version="CURRENT")

flag = 1
merge_counter = 1
wildcard_prfix=''
fcs = feature_class_path_lister(os.path.join(data_location, 'Vectors', GDBNAME+'.gdb'), wcard_search)
#Run recursive merge untill all get into a single feature class
while len(fcs)>1:
    wildcard_prfix = 'tmp'+str(flag)
    fc = [fcs[i:i+merge_feature_count] for i in xrange(0, len(fcs), merge_feature_count)]
    for merge_iterator in fc:
        merge_feature_name = wildcard_prfix+'_'+feature_name+os.path.basename(merge_iterator[0]).rsplit('_',1)[-1]
        merge_output = os.path.join(os.path.join(data_location,'TempMerge.gdb'),merge_feature_name)
        arcpy.Merge_management(merge_iterator,merge_output)
    fcs = feature_class_path_lister(os.path.join(data_location,'TempMerge.gdb'), wildcard_prfix+'*')
    flag+=1
    if merge_counter%50==0:
        print "Completed merger of %s"%str(merge_counter)
    merge_counter+=1
    
final_merged_feature = feature_class_path_lister(os.path.join(data_location,'TempMerge.gdb'), wildcard_prfix+'*')[0]
arcpy.CopyFeatures_management(final_merged_feature, os.path.join(data_location, 'Vectors', GDBNAME+'.gdb\\',merged_feature_name))
arcpy.env.workspace = os.path.join(data_location, 'Vectors', GDBNAME+'.gdb')
shutil.rmtree(os.path.join(data_location,'TempMerge.gdb'))
