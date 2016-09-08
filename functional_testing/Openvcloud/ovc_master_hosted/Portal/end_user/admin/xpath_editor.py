from functional_testing.Openvcloud.ovc_master_hosted.Portal.end_user.page_elements_xpath import account_page
from functional_testing.Openvcloud.ovc_master_hosted.Portal.end_user.page_elements_xpath import xpaths_dic

elements = {}
elements.update(account_page.elements)

duplicate_values_keys = []

for key in elements.keys():
    if key in xpaths_dic.elements.keys():
        if elements[key] == xpaths_dic.elements[key]:
            duplicate_values_keys.append(key)
        else:
            print(key," ",elements[key],"   ",xpaths_dic.elements[key])

print(len(duplicate_values_keys),len(elements))
for key in duplicate_values_keys:
    del elements[key]

if input("0") == str(0):
    print("G")
    Final = open("xpaths_dic.py",'a+')
    Final.write(str(elements))
