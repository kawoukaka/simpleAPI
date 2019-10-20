from flask_restplus import fields

# models for payload validation
# ==============================================================
create_organization_model = {
    "org_name": fields.String(
        required=True,
        description="Organization Name - less than 20 chars",
        example="CameraIQ",
        max_length=20,
    ),
    "org_address": fields.String(
        required=False,
        description="Organization Address - less than 100 chars",
        example="3000 West Peachtree st, Atlanta, GA",
        max_length=100,
    ),
    "org_phone": fields.String(
        required=False,
        description="Organization phone number - less than 14 digits",
        example="(404)1111-1111",
        max_length=14,
    )
}

create_user_model = {
    "user_first_name": fields.String(
        required=True,
        description="User First Name - less than 20 chars",
        example="John",
        max_length=20,
    ),
    "user_last_name": fields.String(
        required=True,
        description="User Last Name - less than 20 chars",
        example="Doe",
        max_length=20,
    ),
    "user_email": fields.String(
        required=True,
        description="User Email - less than 50 chars",
        example="John@att.com",
        max_length=50,
    ),
    "user_address": fields.String(
        required=False,
        description="User Address - less than 100 chars",
        example="3000 West Peachtree st, Atlanta, GA",
        max_length=100,
    ),
    "user_phone": fields.String(
        required=False,
        description="User phone number - less than 14 digits",
        example="(404)1111-1111",
        max_length=14,
    )
}

add_user_to_organization_model = {
    "user_email": fields.String(
        required=True,
        description="User Email - less than 50 chars",
        example="John@att.com",
        max_length=50,
    ),
    "org_name": fields.String(
        required=True,
        description="Organization Name - less than 20 chars",
        example="CameraIQ",
        max_length=20,
    )
}

delete_user_from_organization_model = {
    "user_email": fields.String(
        required=True,
        description="User Email - less than 50 chars",
        example="John@att.com",
        max_length=50,
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
    "user_email": fields.String(
        required=True,
        description="User Email - less than 50 chars",
        example="John@att.com",
        max_length=50,
    ),
}
