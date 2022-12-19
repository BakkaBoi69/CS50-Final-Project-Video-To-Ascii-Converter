# Importing all necessary libraries
import cv2, os
from PIL import Image, ImageFont, ImageDraw
from math import floor
from time import sleep
import moviepy.editor as mp
import ffmpeg, subprocess
from sys import exit
from shutil import rmtree



def main():
    print("Welcome to the video to ascii converter!")
    choice = input("Video (V), Image (I) or Livetext (L): ").upper()
    if choice == "V":
        video()
    elif choice == "I":
        image()
    elif choice == "L":
        video_fp = get_video_fp()
        frames = extract(video_fp)
        fps = get_fps(video_fp)
        # size = int(input("Size of display (in characters): "))
        input("Press enter to start: ")
        livetext(frames, fps)
    else:
        exit("Invalid input: please enter V, I or L")


def get_size():
    try:
        size = int(input("Width of display (in characters; original ratio is preserved): "))
    except ValueError:
        exit("Invalid input: size must be an integer")
    return size


def get_fps(video_fp):
    fps = cv2.VideoCapture(video_fp).get(cv2.CAP_PROP_FPS)
    return fps
    

def get_video_fp():
    ans = input("Enter video filepath: ")
    if os.path.exists(ans):
        return ans
    else: 
        raise FileNotFoundError("The filepath provided for the video doesn't exist")
        #if filepath doesn't exist, raise error and exit


def image():
    image = Image.open("./files/cat.jpeg") # give filepath to target image
    ascii_img, width, height = imgfile(img_to_ascii(greyify(resize(image))), image.size) # width and height 
    ascii_img.save("./test220.png") # saves the image; filepath to destination where it must be saved


def livetext(frames, fps):
    for i in range(frames): #6572 for my video
        print(i) # just prints the frames number; optional
        image = Image.open("./bin/unconverted_frames/frame"+str(i)+".jpeg")
        img_to_ascii(greyify(resize(image, 180)), ('d', fps)) # just plays the ascii images
    rmtree("./bin") # deletes the bin folder
    return None


def video():
    video_fp = get_video_fp()
    fps = get_fps(video_fp)
    frames = extract(video_fp)
    # this extracts the frames of the video into a subfolder and gets the total frames contained in the video
    char_size = get_size()
    if not os.path.exists('bin/frames'):
            os.makedirs('bin/frames')
    for i in range(frames): #6572 for my video
        print(i)
        image = Image.open("./bin/unconverted_frames/frame"+str(i)+".jpeg")
        # convert all unconverted images to ascii images
        ascii_img, width, height = imgfile(img_to_ascii(greyify(resize(image, char_size))), image.size)
        # default size is 200
        ascii_img.save("./bin/frames/test"+str(i)+".jpeg")
    size = (width, height)
    print(size)
    print("Making Video...")
    make_video(frames, size, fps, video_fp) # frames = 6572, size = (1200, 900) for resize width = 100, fps = 30 for my video


def make_video(frame, size, fps, video_fp):
    # creating video file
    if not os.path.exists('bin/output'):
            os.makedirs('bin/output')
    out = cv2.VideoWriter('./bin/output/video.mp4',cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    # just don't touch the VideoWriter_fourcc bit
    for i in range(frame):
        print(i)
        img = cv2.imread(r'./bin/frames/test'+str(i)+'.jpeg')
        # read every ascii frame and write it to a video file
        out.write(img)
    out.release()
    make_audio(video_fp)
    paste_audio()
    rmtree("./bin") # deletes the bin folder
    

def make_audio(video_fp):
    # creating the audio file
    original = mp.VideoFileClip(video_fp)
    original.audio.write_audiofile(r"./bin/output/audio.mp3")


def paste_audio():
    # pasting sound
    # just using ffmpeg because saving the file with moviepy wasn't preserving the audio
    input_video = ffmpeg.input('./bin/output/video.mp4')
    input_audio = ffmpeg.input('./bin/output/audio.mp3')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output('./finished_video.mp4').run()
    

def extract(video_fp):
    # Read the video from specified path
    cam = cv2.VideoCapture(video_fp)

    try:

        # creating a folder named data
        if not os.path.exists('bin/unconverted_frames'):
            os.makedirs('bin/unconverted_frames')

    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of unconverted_frames')

    # frame
    currentframe = 0

    while(True):

        # reading from frame
        ret,frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = './bin/unconverted_frames/frame' + str(currentframe) + '.jpeg'
            print ('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()
    return currentframe


def greyify(image):
    return image.convert(mode="L")


def resize(image, new_width=220):
    # need to resize otherwise the size becomes wayyy to big
    ratio = image.size[1]/image.size[0]
    new_height = ratio * new_width
    new_height = int(new_height)
    return image.resize((new_width, new_height))


def img_to_ascii(image, w=("nothing", 0)):
    pixels = image.getdata()
    width = image.size[0]
    # these are all character sets
    chars = "$@B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`\'  "
    # chars2 = "@#S%?*+;:,."
    # chars3 = chars[::2]
    char_data = "".join([chars[floor(pixel/3.86)]*2 for pixel in pixels])
    # char_data = "".join([chars2[floor(pixel/25)]*2 for pixel in pixels])
    # char_data = "".join([chars3[floor(pixel/7.7)]*2 for pixel in pixels])
    # joining the \n so that not everything is in one line
    ascii_img_data = "\n".join(char_data[i:(i + width*2)] for i in range(0, len(char_data), width*2))
    # this option is reserved for the liveview mode which will play the video in the terminal (no sound)
    if w[0] == 'd':
        # with open("test.txt", 'w') as file:
        #     file.write(ascii_img_data)
        print(ascii_img_data) 
        # print("\n" * 17)
        # you can add \n's to adjust the spacing between frames for a cleaner look in the terminal
        sleep((1/w[1])/1.6)
        subprocess.run("clear")
        # change the sleep parameter depending upon the fps so that video doesn't play too fast
        return None
    else:
        return ascii_img_data


def imgfile(ascii, size):
    ascii_img = Image.new("L", (1, 1), color=255)
    # create an image in greyscale mode, with size 1x1 pixels, and bgc being 255 (white)
    one_line = ""
    # important tool that will help us later
    for i in ascii:
        #getting the string that represents one line of this image
        if i != '\n':
            one_line += i
        else:
            break

    ratio = size[1]/size[0]
    # a surprise that will help us later

    # font = ImageFont.truetype("./files/arial.ttf", 13)
    # a failed font attempt ^
    font = ImageFont.load_default()
    width = font.getbbox(one_line)[2]
    # very important; we get the width in terms of pixels which is very important to resize the image to
    height = floor(ratio * width)
    # since ratio is height/width and multiplying by width will give the height corresponding to it
    ascii_img = ascii_img.resize((width, height))
    # now, resize the image so it is just big enough to contain everything
    draw = ImageDraw.Draw(ascii_img)
    # this is a "draw-er" which will do the drawing
    draw.multiline_text((0,0), ascii, font=font, spacing=2)
    # this does the drawing; starting from (0,0) aka the top left corner; font is whatever; and spacing between lines
    # i.e the vertical spacing between lines is 2. dont touch the spacing
    return ascii_img, width, height
    # returns more than the image because we'll need the size for other functions


if __name__ == "__main__":
    main()