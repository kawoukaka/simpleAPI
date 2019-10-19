from flask_restplus import fields

# models for payload validation
# ==============================================================
create_organization_model = {
    "org_name": fields.String(
        required=True,
        description="Organization Name - less than 20 chars",
        example="CameraIQ",
        max_length=20,
    )
}

create_user_model = {
    "user_name": fields.String(
        required=True,
        description="User Name - less than 20 chars",
        example="John",
        max_length=20,
    )
}

add_user_to_organization_model = {
    "user_name": fields.String(
        required=True,
        description="User Name - less than 20 chars",
        example="John",
        max_length=20,
    ),
    "org_name": fields.String(
        required=True,
        description="Organization Name - less than 20 chars",
        example="CameraIQ",
        max_length=20,
    )
}

delete_user_from_organization_model = {
    "user_name": fields.String(
        required=True,
        description="User Name - less than 20 chars",
        example="John",
        max_length=20,
    ),
    "org_name": fields.String(
        required=True,
        description="Organization Name - less than 20 chars",
        example="CameraIQ",
        max_length=20,
    )
}

get_all_user_model = {
    "org_name": fields.String(
        required=True,
        description="Organization Name - less than 20 chars",
        example="CameraIQ",
        max_length=20,
    )
}

get_all_organization_from_user_model = {
    "user_name": fields.String(
        required=True,
        description="User Name - less than 20 chars",
        example="John",
        max_length=20,
    )
}
