UPDATE_SQLS = {
    'apps' : """update impay_applications set app_name=%(app_name)s, app_rsa_public_key= %(app_rsa_public_key)s where app_id= %(app_id)s""",
}

QUERY_SQLS = {
    'apps' :   """select DATE_FORMAT(created_datetime,'%%Y-%%m-%%d %%H:%%i:%%S') created_datetime,
                                    app_id,
                                    app_name,
                                    platform_rsa_private_key,
                                    platform_rsa_public_key,
                                    app_rsa_public_key,
                                    secret_key
                            from impay_applications
                            order by app_id  desc
                    """,
    'appconf' : """select a.app_id,
                                         a.app_name,
                                         DATE_FORMAT(b.created_datetime,'%%Y-%%m-%%d %%H:%%i:%%S') created_datetime,
                                         DATE_FORMAT(b.updated_datetime,'%%Y-%%m-%%d %%H:%%i:%%S') updated_datetime,
                                         b.pay_type,
                                         b.accounts
                             from impay_app_pay_configs b
                               join impay_applications a
                                       on a.app_id = b.app_id;""",
}

INSERT_SQLS = {
    'apps' : """insert into impay_applications(app_name,
                                                                              platform_rsa_private_key,
                                                                              platform_rsa_public_key,
                                                                              app_rsa_public_key,
                                                                              secret_key)
                                                                values(%(app_name)s,
                                                                             %(platform_rsa_private_key)s,
                                                                             %(platform_rsa_public_key)s,
                                                                             %(app_rsa_public_key)s,
                                                                             %(secret_key)s)""",
}
