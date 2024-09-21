from pymongo import MongoClient
from datetime import datetime

import copy


class DatabaseHandler:
    """
    This class is used to interact with the database in which the
    projects are stored and its information and status is handled.

    The projects are stored in the database containing the mongo
    '_id'', a 'status', the 'script' (that is the whole json used
    to generate it and to compare other json files to check if
    existing), and the 'segments' field that is the one the app
    uses to handle the building data and this process.

    The 'script' must be preserved as it is, to be able to compare
    jsons and avoid duplicated projects, and the 'segments' field
    must be used by the app to keep the building process progress.
    """
    DATABASE_NAME = 'youtube_autonomous'
    CONNECTION_STRING = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false/' + DATABASE_NAME  # previous: youtubeautonomo
    client = None

    def __init__(self):
        # Initialize database connection
        self.get_database()

    def get_database(self):
        """
        Returns the client connected to the database.
        """
        if not self.client:
            self.client = MongoClient(self.CONNECTION_STRING)

        return self.client[self.DATABASE_NAME]
    
    def get_database_projects_table(self):
        """
        Returns the database 'projects' table
        """
        return self.get_database()['projects']
    
    def get_unfinished_project(self):
        """
        Returns the first unfinished project existing in database,
        or None if there are no unfinished projects.

        TODO: Is it actually the first or the last one (?)
        """
        db_projects_table = self.get_database_projects_table()

        db_unfinished_projects = db_projects_table.find({
            "status": { "$ne": "finished" }
        })

        try:
            return db_unfinished_projects.next()
        except:
            return None
    
    def get_unfinished_projects(self):
        """
        Returns the unfinished projects that exist in the
        database or an empty array if there are no unfinished
        projects.
        """
        db_projects_table = self.get_database_projects_table()

        db_unfinished_projects = db_projects_table.find({
            "status": { "$ne": "finished" }
        })

        # Build a projects array
        # TODO: Improve this, please
        projects = []
        do_finish = False
        while not do_finish:
            try:
                projects.append(db_unfinished_projects.next())
            except:
                do_finish = True
                pass

        return projects
    
    # TODO: Apply 'json' type
    def get_database_project_from_json(self, json):
        """
        Returns the project with the provided 'json' that is stored
        in the database if it actually exists. The 'json' is the 
        whole script that builds the video segments.
        """
        db_projects = self.get_database_projects_table()

        db_project = db_projects.find({
            'script': json
        })

        # TODO: Improve this if possible
        try:
            return db_project.next()
        except:
            return None
        
    # TODO: Apply the 'id' type
    def get_database_project_from_id(self, id):
        """
        Returns the project with the given 'id' if available, or None
        if not.
        """
        db_projects = self.get_database_projects_table()

        db_project = db_projects.find({
            '_id': id
        })

        # TODO: Improve this if possible
        try:
            return db_project.next()
        except:
            return None
        
    def insert_project(self, json):
        """
        Creates a new project with the provided 'json' script
        and returns, if successfully inserted, the project 
        object that has been inserted in the database.
        """
        db_project = self.get_database_project_from_json(json)

        if db_project:
            # TODO: Raise exception because it exist
            return None
        
        # TODO: Maybe improve the wrong format checkings
        if not 'segments' in json:
            # TODO: Raise exception because wrong format
            return None
        
        script = copy.deepcopy(json)

        segments = []
        for segment in json['segments']:
            segment['status'] = 'to_start'
            segment['created_at'] = datetime.now()
            segments.append(segment)

        # Lets separate each segment and build the statuses
        data = {
            'status': 'to_start',
            'script': script,
            'segments': segments
        }

        db_projects_table = self.get_database_projects_table()
        db_project_id = db_projects_table.insert_one(data).inserted_id
        
        return self.get_database_project_from_id(db_project_id)
    
    def __update_project_segment_field(self, db_project_id, segment_index, field, value):
        """
        Updates a segment field from the provided project (identified by 
        'project_id').
        """
        if segment_index < 0:
            raise Exception('In valid "segment_index" provided')
        
        # TODO: Improve checkings
        query = { '_id': db_project_id }
        new_values = { "$set": { 'segments.' + str(segment_index) + '.' + field: value } }

        db_projects_table = self.get_database_projects_table()
        db_projects_table.update_one(query, new_values)

    def __update_project_segment_status(self, db_project_id, segment_index, status):
        self.__update_project_segment_field(db_project_id, segment_index, 'status', status)

    def set_project_segment_as_in_progress(self, db_project_id, segment_index):
        # TODO: Make 'in_progress' a constant
        self.__update_project_segment_status(db_project_id, segment_index, 'in_progress')

    def set_project_segment_as_finished(self, db_project_id, segment_index):
        # TODO: Make 'finished' a constant
        self.__update_project_segment_status(db_project_id, segment_index, 'finished')
        self.__update_project_segment_field(db_project_id, segment_index, 'finished_at', datetime.now())

    def set_project_segment_transcription(self, db_project_id, segment_index, transcription):
        self.__update_project_segment_field(db_project_id, segment_index, 'transcription', transcription)

    def set_project_segment_audio_filename(self, db_project_id, segment_index, audio_filename):
        self.__update_project_segment_field(db_project_id, segment_index, 'audio_filename', audio_filename)

    def set_project_segment_video_filename(self, db_project_id, segment_index, video_filename):
        self.__update_project_segment_field(db_project_id, segment_index, 'video_filename', video_filename)

    def set_project_segment_full_filename(self, db_project_id, segment_index, full_filename):
        self.__update_project_segment_field(db_project_id, segment_index, 'full_filename', full_filename)

    def __update_project_field(self, db_project_id, field, value):
        db_project = self.get_database_project_from_id(db_project_id)

        if not db_project:
            return None
        
        db_projects_table = self.get_database_projects_table()
        query = { '_id': db_project_id }
        new_values = { "$set": { field: value } }
        db_projects_table.update_one(query, new_values)

    def set_project_music_filename(self, db_project_id, music_filename):
        self.__update_project_field(db_project_id, 'music_filename', music_filename)

    def set_project_as_in_progress(self, db_project_id):
        """
        Sets the project (identified by 'db_project_id') status as 
        'in_progress'.
        """
        # TODO: Make 'in_progress' a constant
        self.__update_project_field(db_project_id, 'status', 'in_progress')

    def set_project_as_finished(self, db_project_id):
        """
        Sets the project (identified by 'db_project_id') status as
        'finished'.
        """
        self.__update_project_field(db_project_id, 'status', 'finished')
