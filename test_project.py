import project
import mock
import builtins
import pytest


# Mocking the input function since it doesn't take any arguments
def test_get_size():
    with mock.patch.object(builtins, 'input', lambda _: '200'):
        assert project.get_size() == 200
    
    with mock.patch.object(builtins, 'input', lambda _: 'cat'):
        with pytest.raises(SystemExit):
            project.get_size()
    
    with mock.patch.object(builtins, 'input', lambda _: '10'):
         with pytest.raises(SystemExit):
            project.get_size()
     
        
# testing both functions that get the filepaths    
def test_get_image_fp():
    with mock.patch.object(builtins, 'input', lambda _: './test_files/cat.jpeg'):
        assert project.get_image_fp() == './test_files/cat.jpeg'
    
    with mock.patch.object(builtins, 'input', lambda _: 'cat.jpeg'):
        with pytest.raises(FileNotFoundError):
            project.get_image_fp()


def test_get_video_fp():
    with mock.patch.object(builtins, 'input', lambda _: './test_files/BadApple.mp4'):
        assert project.get_video_fp() == './test_files/BadApple.mp4'
    
    with mock.patch.object(builtins, 'input', lambda _: 'cat.mp4'):
        with pytest.raises(FileNotFoundError):
            project.get_video_fp()
            
            
# testing the get_fps function
def test_get_fps():
    assert project.get_fps('./test_files/BadApple.mp4') == 30
    
    with pytest.raises(SystemExit):
        project.get_fps('./test_files/cat.jpeg')
        
