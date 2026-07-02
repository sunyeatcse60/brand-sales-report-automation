# # import brand_report
# # import upload_to_sheet

# # print("Automation Finished")



# from brand_report import (
#     login,
#     create_wizard,
#     generate_report,
#     download_report
# )

# from upload_to_sheet import upload_excel_to_sheet


# def main():

#     uid = login()

#     wizard_id = create_wizard(uid)

#     report = generate_report(uid, wizard_id)

#     excel_file = download_report(report)

#     upload_excel_to_sheet(excel_file)

#     print("Automation Finished Successfully")


# if __name__ == "__main__":
#     main()

from brand_report import (
    REPORTS,
    login,
    create_wizard,
    generate_report,
    download_report,
)

from upload_to_sheet import upload_excel_to_sheet


def main():

    uid = login()

    for report_type, sheet_name in REPORTS.items():

        print("=" * 80)
        print(f"Generating : {sheet_name}")
        print("=" * 80)

        wizard_id = create_wizard(uid, report_type)

        report = generate_report(uid, wizard_id)

        excel_file = download_report(report, report_type)

        upload_excel_to_sheet(excel_file, sheet_name)

        print(f"{sheet_name} Completed\n")

    print("=" * 80)
    print("All Reports Completed Successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()