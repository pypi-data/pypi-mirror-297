from .db_config import LOCAL_SQLITE_DB, LOCAL_POSTGRES_DB, AWS_POSTGRES_DB

environments = {
    "dev": {
        "db": {
            "default": LOCAL_SQLITE_DB,
            "secondary": LOCAL_POSTGRES_DB,
            "cloud": AWS_POSTGRES_DB,
        },
        "secret_key": 'django-insecure-o=%em30v3%(+r1(_+hss!sbnf5!!7#0+#wr8o%wnxm5i9u6snx',
        "s3_files": False,
    },
    "test": {
        "db": {
            "default": LOCAL_POSTGRES_DB,
            "secondary": LOCAL_SQLITE_DB,
            "cloud": AWS_POSTGRES_DB,
        },
        "secret_key": "3t3@9pfd&38abb-6!-1@)8qkiym#m&3rez6y@twb2m-famp%@z",
        "s3_files": False,
    },
    "prod": {
        "db": {
            "default": AWS_POSTGRES_DB,
        },
        "secret_key": ")71f$am49cs0q*dtmi(49a9s6)iw8s*hjgc(7sa@8mgk-t&!&$",
        "s3_files": True,

    },
}
