def test_report_generation__success(generate_report_service, generate_report_entity):
    generate_report_service.generate_report(generate_report_entity, user_id=3)

