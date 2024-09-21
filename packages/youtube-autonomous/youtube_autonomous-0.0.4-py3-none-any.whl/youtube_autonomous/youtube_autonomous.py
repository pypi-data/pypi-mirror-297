from yta_general_utils.temp import clean_temp_folder
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.path import create_file_abspath
from yta_general_utils.file.reader import read_json_from_file
from yta_general_utils.logger import print_completed
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.segments.validation.segment_validator import SegmentValidator
from typing import Union


class YoutubeAutonomous:
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.
    """
    __segment_validator: SegmentValidator = None
    """
    Object to validate the segments we want to use to build a project.
    """
    segments_abspath: Union[str, None] = None
    """
    The absolute path that points to the segments folder in which this
    software will store the segments related content parts that are
    created during the whole segment building process. This folder 
    allows us recovering a non-finished project in which we generated
    some segments in the past but not all of them.
    """

    def __init__(self, segments_abspath: Union[str, None] = None):
        """
        Initializes the object by creating the segments files folder
        in the provided 'segments_abspath' if it doesn't exist. This
        parameter, if not provided, will make the folder be created
        in the current project main folder with 'segments_files' 
        folder name.
        """
        self.__database_handler = DatabaseHandler()
        self.__segment_validator = SegmentValidator()

        if not segments_abspath:
            segments_abspath = get_project_abspath() + 'segments_files'
        
        # TODO: Do some checkings about the provided abspath
        self.segments_abspath = segments_abspath
        # We force to create the folder if it doesn't exist
        create_file_abspath(self.segments_abspath + 'toforce')

    def purge(self, do_remove_segments_files = False):
        """
        Cleans the temporary folder removing all previous generated 
        temporary files, and also the segment files if the
        'do_remove_segments_files' parameter is set to True.
        """
        clean_temp_folder()
        if do_remove_segments_files:
            # TODO: Remove all files in self.segments_abspath folder
            pass

    def check_config(self):
        # TODO: Check that he config is ok
        pass
     
    def insert_project_in_database_from_file(self, filename: str):
        """
        Reads the provided project content 'filename' and creates a new 
        project in the database if the provided 'filename' contains a new
        project and is valid. If the information belongs to an already
        registered project, it will raise an exception.

        This method returns the new stored project mongo ObjectId if 
        successfully stored, or raises an Exception if anything went wrong.
        """
        if not filename:
            raise Exception('We need a project content "filename" to create a new project.')
        
        if not isinstance(filename, str):
            raise Exception('The "filename" parameter provided is a str.')
        
        json_data = self.__read_project_from_file(filename)

        # If a project with the same content exists, it is the same project
        db_project = self.__database_handler.get_database_project_from_json(json_data)
        if db_project:
            raise Exception('There is an existing project in the database with the same content.')

        db_project = self.__database_handler.insert_project(json_data)

        print_completed('Project created in database with ObjectId = "' + str(db_project['_id']) + '"')

        return str(db_project['_id'])
    
    # TODO: This below is for testing, remove it
    def get_unfinished_project(self):
        """
        Returns the first unfinished project that exists in the
        database, or None if there are no unfinished projects.
        """
        return self.__database_handler.get_unfinished_project()

    def get_unfinished_projects(self):
        """
        Returns a list containing all the existing projects in the 
        database that have not been finished yet, or an empty list
        if there are no unfinished projects.
        """
        return self.__database_handler.get_unfinished_projects()
    
    def __read_project_from_file(self, filename: str):
        """
        Reads the provided 'filename', that should contain the information of
        a project, and validates its content and structure. This method will
        return the data read as a dict or will raise an Exception if something
        is not ok.
        """
        if not filename:
            raise Exception('No "filename" provided.')
        
        if not isinstance(filename, str):
            raise Exception('The "filename" parameter provided is a str.')
        
        json_data = read_json_from_file(filename)

        if not 'segments' in json_data:
            raise Exception('The provided "filename" does not contain the expected data structure.')

        # We validate each segment to be able to store the project
        # This will raise an Exception if something is not ok
        for segment in json_data['segments']:
            self.__segment_validator.validate(segment)

        return json_data

    # TODO: Apply ObjectId type to 'project_id'
    def __get_project_from_database_by_id(self, project_id):
        """
        Gets the project with the provided 'project_id' if existing, or
        None if not.
        """
        return self.__database_handler.get_database_project_from_id(project_id)
    
    # TODO: Apply json type to 'json'
    def __get_project_from_database_by_json(self, json):
        """
        Gets the project with the provided 'json' if existing, or None if
        not. This 'json' will be compared with the 'script' field stored
        in database to check if there is a similar project previously 
        stored that must be recovered instead of duplicating it.
        """
        return self.__database_handler.get_database_project_from_json(json)
