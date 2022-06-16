from cgi import test


test_string=  "A /IVVPr/IVVPr_SWA/Tests/Developing/Testing_Procedures_for_SCADE/P_DATA_SOURCE_CHOICE/MC21_SWA_M_FWS_CHOICE/MC21_SWA_M_FWS_CHOICE.csv (from /IVVPr/IVVPr_SWA/Tests/Developing/Testing_Procedures_for_SCADE/P_DATA_SOURCE_CHOICE/MC21_SWA_M_FWS_CHOICE/MC21_SWA_M_FWS_CHOICE.csv:18223)"

if '(from' in test_string:
   test_string = test_string.split('(from')[0]
   print(test_string)
   
