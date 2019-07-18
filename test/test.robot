*** Settings ***
Library    ScreenCompareLibrary
Library    SeleniumLibrary
Library    OperatingSystem
Test Teardown    Close Browser

*** Test Cases ***
Test Screen Comparision Valid
    Open Browser    https://www.orange.sk
    Set Window Size    1920    1080
#    Maximize Browser Window
    Capture Page Screenshot    to_compare.png
    ${res}    Compare Screenshots    to_compare.png    google.png
    Should Be True    ${res}

Test Screen Comparision Invalid
    Open Browser    https://www.root.cz
    Maximize Browser Window
    ${path}    Capture Page Screenshot    to_compare.png
    Run Keyword And Expect Error    Images are not the same    Compare Screenshots    to_compare.png    google.png    diff.png
    File Should Exist    diff.png

Test Compare Folders
    Compare Folders    Actual    Original    True


Test Find If Image Contains Another Image And Save Result
    Open Browser    https://www.root.cz
    Maximize Browser Window
    ${path}    Capture Page Screenshot    within.png
    Find Image Location    within.png    inimage.png    result=result_compare.png    treshold=0.8
    File Should Exist    result_compare.png

Test Find If Image Does not Contains Another Image
    Open Browser    https://www.sme.sk
    Maximize Browser Window
    ${path}    Capture Page Screenshot    within.png
    Run Keyword And Expect Error    Image is not within source image    Find Image Location    within.png    aaa.png    result=result_compare.png    treshold=0.8