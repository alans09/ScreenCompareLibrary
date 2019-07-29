*** Settings ***
Library    ScreenCompareLibrary   1024,768
Library    SeleniumLibrary
Library    OperatingSystem
Test Teardown    Close Browser

*** Test Cases ***
Test Screen Comparision Valid
    Open Browser    https://robotframework.org/#examples
    Set Window Size    1920    1080
    Wait Until Element Is Visible    css=span.nf:nth-child(44)
    Capture Page Screenshot    to_compare.png
    ${res}    Compare Screenshots    to_compare.png    rf.png
    Should Be True    ${res}

Test Screen Comparision Invalid
    [Tags]    test
    Open Browser    https://www.root.cz
    Maximize Browser Window
    ${path}    Capture Page Screenshot    to_compare.png
    ${res}    Compare Screenshots    to_compare.png    rf.png    diff.png
    Should Not Be True    ${res}
    File Should Exist    diff.png

Test Compare Folders
    ${res}    Compare Folders    Actual    Original    True
    Should Be True    ${res}


Test Find If Image Contains Another Image And Save Result
    Open Browser    https://robotframework.org/#examples
    Set Window Size    1920    1080
    ${path}    Capture Page Screenshot    within.png
    ${res}    Find Image Location    within.png    rf_small.png    result=result_compare.png    threshold=0.8
    Should Be True    ${res}
    File Should Exist    result_compare.png

Test Find If Image Does Not Contains Another Image
    Open Browser    https://www.sme.sk
    Maximize Browser Window
    ${path}    Capture Page Screenshot    within.png
    ${res}    Find Image Location    within.png    aaa.png    result=result_compare.png    threshold=0.8
    Should Not Be True    ${res}
    File Should Exist    result_compare.png