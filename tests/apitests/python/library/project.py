# -*- coding: utf-8 -*-

import sys
import base
import swagger_client

class Project(base.Base):
    def create_project(self, name=None, metadata=None, **kwargs):
        if name is None:
            name = base._random_name("project")
        if metadata is None:
            metadata = {}
        client = self._get_client(**kwargs)
        _, status_code, header = client.projects_post_with_http_info(
            swagger_client.ProjectReq(name, metadata))
        base._assert_status_code(201, status_code)
        project_id = base._get_id_from_header(header)
        return name, project_id

    def get_projects(self, params, **kwargs):
        client = self._get_client(**kwargs)
        data = []
        data, status_code, _ = client.projects_get_with_http_info(**params)
        base._assert_status_code(200, status_code)
        return data

    def projects_should_exist(self, params, expected_count = None, expected_project_id = None, **kwargs):
        project_data = self.get_projects(params, **kwargs)
        actual_count = len(project_data)
        if expected_count is not None and actual_count!= expected_count:
            raise Exception(r"Private project count should be {}.".format(expected_count))
        if expected_project_id is not None and actual_count == 1 and str(project_data[0].project_id) != str(expected_project_id):
            raise Exception(r"Project-id check failed, expect {} but got {}, please check this test case.".format(str(expected_project_id), str(project_data[0].project_id)))

    def check_project_name_exist(self, name=None, **kwargs):
        client = self._get_client(**kwargs)
        _, status_code, _ = client.projects_head_with_http_info(name)
        return {
            200: True,
            404: False,
        }.get(status_code,'error')


    def get_project(self, project_id, **kwargs):
        client = self._get_client(**kwargs)
        data, status_code, _ = client.projects_project_id_get_with_http_info(project_id)
        base._assert_status_code(200, status_code)
        return data

    def update_project(self, project_id, metadata, **kwargs):
        client = self._get_client(**kwargs)
        project = swagger_client.Project(project_id, None, None, None, None, None, None, None, None, None, None, metadata)
        _, status_code, _ = client.projects_project_id_put_with_http_info(project_id, project)
        base._assert_status_code(200, status_code)

    def delete_project(self, project_id, expect_status_code = 200, **kwargs):
        client = self._get_client(**kwargs)
        _, status_code, _ = client.projects_project_id_delete_with_http_info(project_id)
        base._assert_status_code(expect_status_code, status_code)

    def get_project_metadata_by_name(self, project_id, meta_name, **kwargs):
        client = self._get_client(**kwargs)
        ProjectMetadata = swagger_client.ProjectMetadata()
        ProjectMetadata, status_code, _ = client.projects_project_id_metadatas_meta_name_get_with_http_info(project_id, meta_name)
        base._assert_status_code(200, status_code)
        return {
            'public': ProjectMetadata.public,
            'enable_content_trust': ProjectMetadata.enable_content_trust,
            'prevent_vul': ProjectMetadata.prevent_vul,
            'auto_scan': ProjectMetadata.auto_scan,
            'severity': ProjectMetadata.severity,
        }.get(meta_name,'error')

    def get_project_members(self, project_id, **kwargs):
        client = self._get_client(**kwargs)
        data = []
        data, status_code, _ = client.projects_project_id_members_get_with_http_info(project_id)
        base._assert_status_code(200, status_code)
        return data

    def add_project_members(self, project_id, user_id, member_role_id = None, expect_status_code = 201, **kwargs):
        if member_role_id is None:
            member_role_id = 1
        _member_user = {"user_id": int(user_id)}
        projectMember = swagger_client.ProjectMember(member_role_id, member_user = _member_user)
        client = self._get_client(**kwargs)
        data = []
        data, status_code, _ = client.projects_project_id_members_post_with_http_info(project_id, project_member = projectMember)
        base._assert_status_code(201, status_code)
        return data