*** Settings ***
Library    ScreenCompareLibrary
Library    SeleniumLibrary
Library    OperatingSystem
Test Teardown    Close Browser

*** Test Cases ***
Test Screen Comparision Valid
    Open Browser    https://www.google.sk
    Maximize Browser Window
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
