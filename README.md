0.
your env var should have ${GERRIT_PASSWORD}, which is your gerrit account id password
edit create_projects.py
change my account(10064088) to your account

1.
edit projects_info.txt
you can put many projects here.
after : is group name.
for example:
Power-RD-Projects/ZXDUPA-PMSC:power-pmsc
the project is Power-RD-Projects/ZXDUPA-PMSC
the group is power-pmsc
this script will genenate three groups for you:
power-pmsc-admin
power-pmsc-core
power-pmsc-team

2.
python create_projects.py
is ok

the project_config.template is the relationship template
change project_config.template, you will have a brand-new project-group relationship!


