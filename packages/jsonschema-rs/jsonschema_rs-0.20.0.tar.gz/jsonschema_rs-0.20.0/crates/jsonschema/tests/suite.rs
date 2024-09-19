use jsonschema::Draft;
use std::fs;
use testsuite::{suite, Test};

#[suite(
    path = "crates/jsonschema/tests/suite",
    drafts = [
        "draft4",
        "draft6",
        "draft7",
        "draft2019-09",
        "draft2020-12",
    ],
    xfail = [
        "draft4::optional::bignum::integer::a_bignum_is_an_integer",
        "draft4::optional::bignum::integer::a_negative_bignum_is_an_integer",
        "draft4::optional::ecmascript_regex",
        "draft6::optional::ecmascript_regex",
        "draft7::optional::ecmascript_regex",
        "draft7::optional::format::idn_hostname::validation_of_internationalized_host_names",
        "draft7::optional::format::time::validation_of_time_strings",
        "draft2019-09::anchor",
        "draft2019-09::defs",
        "draft2019-09::optional::anchor",
        "draft2019-09::optional::cross_draft::refs_to_historic_drafts_are_processed_as_historic_drafts",
        "draft2019-09::optional::ecmascript_regex::d_in_pattern_properties_matches_0_9_not_unicode_digits",
        "draft2019-09::optional::ecmascript_regex::w_in_pattern_properties_matches_a_za_z0_9_not_unicode_letters",
        "draft2019-09::optional::format::duration::validation_of_duration_strings",
        "draft2019-09::optional::format::idn_hostname::validation_of_internationalized_host_names",
        "draft2019-09::optional::format::time::validation_of_time_strings",
        "draft2019-09::optional::ref_of_unknown_keyword::reference_internals_of_known_non_applicator",
        "draft2019-09::r#ref::order_of_evaluation_id_and_anchor_and_ref",
        "draft2019-09::r#ref::ref_with_recursive_anchor",
        "draft2019-09::r#ref::urn_base_uri_with_urn_and_anchor_ref",
        "draft2019-09::recursive_ref",
        "draft2019-09::ref_remote::anchor_within_remote_ref",
        "draft2019-09::ref_remote::base_uri_change_change_folder",
        "draft2019-09::ref_remote::location_independent_identifier_in_remote_ref",
        "draft2019-09::ref_remote::ref_to_ref_finds_detached_anchor",
        "draft2019-09::unevaluated_items",
        "draft2019-09::unevaluated_properties::unevaluated_properties_with_recursive_ref",
        "draft2019-09::vocabulary::schema_that_uses_custom_metaschema_with_with_no_validation_vocabulary",
        "draft2020-12::anchor",
        "draft2020-12::defs::validate_definition_against_metaschema::invalid_definition_schema",
        "draft2020-12::dynamic_ref",
        "draft2020-12::optional::anchor::anchor_inside_an_enum_is_not_a_real_identifier",
        "draft2020-12::optional::cross_draft::refs_to_historic_drafts_are_processed_as_historic_drafts",
        "draft2020-12::optional::dynamic_ref::dynamic_ref_skips_over_intermediate_resources_pointer_reference_across_resource_boundary",
        "draft2020-12::optional::ecmascript_regex::a_is_not_an_ecma_262_control_escape",
        "draft2020-12::optional::ecmascript_regex::d_in_pattern_properties_matches_0_9_not_unicode_digits",
        "draft2020-12::optional::ecmascript_regex::w_in_pattern_properties_matches_a_za_z0_9_not_unicode_letters",
        "draft2020-12::optional::format::duration::validation_of_duration_strings",
        "draft2020-12::optional::format::email::validation_of_e_mail_addresses",
        "draft2020-12::optional::format::idn_hostname::validation_of_internationalized_host_names",
        "draft2020-12::optional::format::iri::validation_of_ir_is",
        "draft2020-12::optional::format::iri_reference::validation_of_iri_references::an_invalid",
        "draft2020-12::optional::format::json_pointer::validation_of_json_pointers_json_string_representation",
        "draft2020-12::optional::format::relative_json_pointer::validation_of_relative_json_pointers_rjp",
        "draft2020-12::optional::format::time::validation_of_time_strings",
        "draft2020-12::optional::format::uri_reference::validation_of_uri_references::an_invalid",
        "draft2020-12::optional::format::uri_template::format_uri_template::an_invalid_uri",
        "draft2020-12::optional::ref_of_unknown_keyword::reference_internals_of_known_non_applicator",
        "draft2020-12::r#ref::order_of_evaluation_id_and_anchor_and_ref",
        "draft2020-12::r#ref::urn_base_uri_with_urn_and_anchor_ref",
        "draft2020-12::ref_remote::anchor_within_remote_ref",
        "draft2020-12::ref_remote::base_uri_change_change_folder",
        "draft2020-12::ref_remote::location_independent_identifier_in_remote_ref",
        "draft2020-12::ref_remote::ref_to_ref_finds_detached_anchor",
        "draft2020-12::unevaluated_properties::unevaluated_properties_with_dynamic_ref",
        "draft2020-12::unevaluated_items",
        "draft2020-12::vocabulary",
    ]
)]
fn test_suite(test: Test) {
    let mut options = jsonschema::options();
    match test.draft {
        "draft4" => {
            options.with_draft(Draft::Draft4);
        }
        "draft6" => {
            options.with_draft(Draft::Draft6);
        }
        "draft7" => {
            options.with_draft(Draft::Draft7);
        }
        "draft2019-09" | "draft2020-12" => {}
        _ => panic!("Unsupported draft"),
    };
    if test.is_optional {
        options.should_validate_formats(true);
    }
    let validator = options
        .build(&test.schema)
        .expect("Failed to build a schema");
    let result = validator.validate(&test.data);

    if test.valid {
        if let Err(mut errors_iterator) = result {
            let first_error = errors_iterator.next();
            assert!(
                first_error.is_none(),
                "Test case should not have validation errors:\nGroup: {}\nTest case: {}\nSchema: {}\nInstance: {}\nError: {:?}",
                test.case,
                test.description,
                test.schema,
                test.data,
                first_error,
            );
        }
        assert!(
            validator.is_valid(&test.data),
            "Test case should be valid:\nCase: {}\nTest: {}\nSchema: {}\nInstance: {}",
            test.case,
            test.description,
            test.schema,
            test.data,
        );
        let output = validator.apply(&test.data).basic();
        assert!(
            output.is_valid(),
            "Test case should be valid via basic output:\nCase: {}\nTest: {}\nSchema: {}\nInstance: {}\nError: {:?}",
            test.case,
            test.description,
            test.schema,
            test.data,
            output
        );
    } else {
        assert!(
            result.is_err(),
            "Test case should have validation errors:\nCase: {}\nTest: {}\nSchema: {}\nInstance: {}",
            test.case,
            test.description,
            test.schema,
            test.data,
        );
        let errors = result.unwrap_err();
        for error in errors {
            let pointer = error.instance_path.to_string();
            assert_eq!(
                test.data.pointer(&pointer), Some(&*error.instance),
                "Expected error instance did not match actual error instance:\nCase: {}\nTest: {}\nSchema: {}\nInstance: {}\nExpected pointer: {:#?}\nActual pointer: {:#?}",
                test.case,
                test.description,
                test.schema,
                test.data,
                &*error.instance,
                &pointer,
            );
        }
        assert!(
            !validator.is_valid(&test.data),
            "Test case should be invalid:\nCase: {}\nTest: {}\nSchema: {}\nInstance: {}",
            test.case,
            test.description,
            test.schema,
            test.data,
        );
        let output = validator.apply(&test.data).basic();
        assert!(
            !output.is_valid(),
            "Test case should be invalid via basic output:\nCase: {}\nTest: {}\nSchema: {}\nInstance: {}",
            test.case,
            test.description,
            test.schema,
            test.data,
        );
    }
}

#[test]
fn test_instance_path() {
    let expectations: serde_json::Value =
        serde_json::from_str(include_str!("draft7_instance_paths.json")).expect("Valid JSON");
    for (filename, expected) in expectations.as_object().expect("Is object") {
        let test_file = fs::read_to_string(format!("tests/suite/tests/draft7/{}", filename))
            .unwrap_or_else(|_| panic!("Valid file: {}", filename));
        let data: serde_json::Value = serde_json::from_str(&test_file).expect("Valid JSON");
        for item in expected.as_array().expect("Is array") {
            let suite_id = item["suite_id"].as_u64().expect("Is integer") as usize;
            let schema = &data[suite_id]["schema"];
            let validator = jsonschema::validator_for(schema).unwrap_or_else(|_| {
                panic!(
                    "Valid schema. File: {}; Suite ID: {}; Schema: {}",
                    filename, suite_id, schema
                )
            });
            for test_data in item["tests"].as_array().expect("Valid array") {
                let test_id = test_data["id"].as_u64().expect("Is integer") as usize;
                let instance_path: Vec<&str> = test_data["instance_path"]
                    .as_array()
                    .expect("Valid array")
                    .iter()
                    .map(|value| value.as_str().expect("A string"))
                    .collect();
                let instance = &data[suite_id]["tests"][test_id]["data"];
                let error = validator
                    .validate(instance)
                    .expect_err(&format!(
                        "\nFile: {}\nSuite: {}\nTest: {}",
                        filename,
                        &data[suite_id]["description"],
                        &data[suite_id]["tests"][test_id]["description"],
                    ))
                    .next()
                    .expect("Validation error");
                assert_eq!(
                    error.instance_path.clone().into_vec(),
                    instance_path,
                    "\nFile: {}\nSuite: {}\nTest: {}\nError: {}",
                    filename,
                    &data[suite_id]["description"],
                    &data[suite_id]["tests"][test_id]["description"],
                    &error
                )
            }
        }
    }
}
