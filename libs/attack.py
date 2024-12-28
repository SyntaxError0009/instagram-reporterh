def report_video(ses, res, video_url, report_headers):
    if '"hsi":' not in res.text:
        print_error("Connection error has occurred! (CookieErrorHsi)")
        return

    try:
        if '"LSD",' in res.text:
            lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        else:
            print_error("LSD token not found!")
            return

        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"', "")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"', "")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"', "")

        if "datr" in res.cookies.get_dict():
            datr = res.cookies.get_dict()["datr"]
        else:
            print_error("DATR cookie is missing!")
            return
    except IndexError:
        print_error("Connection error has occurred! (CookieParsingError)")
        return

    report_cookies = {
        "datr": datr
    }

    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "sneakyhidden": "",
        "Field419623844841592": video_url,
        "Field1476905342523314_iso2_country_code": "IN",
        "Field1476905342523314": "India",
        "support_form_id": "440963189380968",
        "support_form_hidden_fields": '{"423417021136459":false,"419623844841592":false,"754839691215928":false,"1476905342523314":false,"284770995012493":true,"237926093076239":false}',
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }

    try:
        res = ses.post(
            "https://help.instagram.com/ajax/help/contact/submit/page",
            data=report_form,
            headers=report_headers,
            cookies=report_cookies,
            timeout=10
        )
    except requests.exceptions.Timeout:
        print_error("Request timed out!")
        return
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        return

    if res.status_code != 200:
        print_error(f"Request failed! Status Code: {res.status_code}")
        return

    print_success("Successfully reported!")
