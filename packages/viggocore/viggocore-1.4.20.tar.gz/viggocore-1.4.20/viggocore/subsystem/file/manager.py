import flask
import uuid
import os
from werkzeug import utils as werkzeug_utils

from viggocore.common.exception import BadRequest
from viggocore.common.subsystem import manager
from viggocore.common.subsystem import operation


# TODO(samueldmq): put this in the app config
UPLOAD_FOLDER = 'uploads'


class Create(operation.Create):

    def __call__(self, file, **kwargs):
        self.file = file
        self.domain_id = kwargs.get('domain_id', None)
        self.user_id = kwargs.pop('user_id', None)
        self.is_internal = type(self.file).__name__ == 'BufferedWriter' \
            or type(self.file).__name__ == 'BufferedReader'
        self.is_reader = type(self.file).__name__ == 'BufferedReader'
        self.filename = self.file.name \
            if self.is_internal else self.file.filename
        return super().__call__(**kwargs)

    def pre(self, session, **kwargs):
        if self.file and self.manager.allowed_file(self.filename):
            filename = werkzeug_utils.secure_filename(self.filename)

            if 'id' not in kwargs.keys():
                kwargs['id'] = uuid.uuid4().hex
            kwargs['created_by'] = self.user_id
            kwargs['name'] = filename
            # TODO note that kwargs must contain olny entity fields
            self.entity = self.driver.instantiate(**kwargs)
        else:
            e = BadRequest()
            e.message = 'file not allowed'
            raise e
        self.upload_folder = self.manager.get_upload_folder(self.entity,
                                                            self.domain_id)
        return self.entity.is_stable()

    def do(self, session, **kwargs):
        if not self.is_internal:
            self.file.save(os.path.join(
                self.upload_folder, self.entity.filename))
        elif self.is_reader:
            with open(
                os.path.join(
                    self.upload_folder, self.entity.filename), 'wb') as file:
                file.write(self.file.read())
        entity = super().do(session)
        return entity


class Get(operation.Get):

    def do(self, session, **kwargs):
        file = super().do(session, **kwargs)

        folder = self.manager.get_upload_folder(file, file.domain_id)
        # folder = get_upload_folder(file.domain_id)
        return flask.send_from_directory(folder, file.filename)


class Manager(manager.Manager):

    OPTIONAL_FOLDER = ''
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv']

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
        self.get = Get(self)

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in cls.ALLOWED_EXTENSIONS

    @classmethod
    def get_upload_folder(cls, entity, domain_id):
        base_folder = cls._get_base_folder()
        entity_name = type(entity).__name__
        folder = os.path.join(base_folder,
                              entity_name,
                              cls.OPTIONAL_FOLDER,
                              domain_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    @classmethod
    def _get_base_folder(cls):
        env_folder = os.environ.get('VIGGOCORE_FILE_DIR', UPLOAD_FOLDER)
        if not os.path.isabs(env_folder):
            env_folder = os.path.join(os.getcwd(), env_folder)
        return env_folder
