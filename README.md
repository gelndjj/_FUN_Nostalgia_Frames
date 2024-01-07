<a name="readme-top"></a>

[![Contributors][contributors-shield]](https://github.com/gelndjj/Nostalgia_Frames/graphs/contributors)
[![Forks][forks-shield]](https://github.com/gelndjj/Nostalgia_Frames/forks)
[![Stargazers][stars-shield]](https://github.com/gelndjj/Nostalgia_Frames/stargazers)
[![Issues][issues-shield]](https://github.com/gelndjj/Nostalgia_Frames/issues)
[![MIT License][license-shield]](https://github.com/gelndjj/Nostalgia_Frames/blob/main/LICENSE)
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/jonathanduthil/)


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/gelndjj/Nostalgia_Frames">
    <img src="https://github.com/gelndjj/Nostalgia_Frames/blob/main/resources/image0.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Nostalgia Frames</h3>

  <p align="center">
    Archive Management Tool
    <br />
    <a href="https://github.com/gelndjj/Nostalgia_Frames"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/gelndjj/Nostalgia_Frames/issues">Report Bug</a>
    ·
    <a href="https://github.com/gelndjj/Nostalgia_Frames/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>

  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
<div align="center">
<img src="https://github.com/gelndjj/Nostalgia_Frames/blob/main/resources/image0.png" alt="Logo" width="128" height="128">
</br>
Nostalgia Frames is a desktop application designed for retro gaming enthusiasts to create and manage game overlays. This tool allows users to manage image overlays, edit CSV files for system configurations, and customize settings for their retro gaming setup.</br>
<img src="https://github.com/gelndjj/Nostalgia_Frames/blob/main/resources/app_osx.png" alt="Screenshot" width="762" height="490">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SCREENSHOTS -->
## Screenshots (MAC OS)

<!-- PREREQUISITES -->

## Getting Started
To get started with the Nostalgia Frames, you will need to clone the repository to your local machine. Ensure you have Python and the necessary libraries installed.

### Prerequisites
- Python 3.x
- PIL (Python Imaging Library)
- Tkinter (usually bundled with Python)

<!-- USAGE EXAMPLES -->
# Usage Documentation

## Usage

### Loading Images
1. Click on the `Load Pictures` button.
2. Select a folder containing your .png images.
3. The images will be displayed in the left panel of the application.

### Creating Overlays
1. Select an image from the list.
2. Adjust the width and height in the provided fields if necessary.
3. Click the `Create Overlay` button to generate the overlay.
4. The overlay and the corresponding .cfg file will be saved in the current directory.

### Editing System Configurations
1. Click on the `Edit CSV` button to modify the system configurations.
2. A new window will open displaying the current configurations from `Resolutions integer scaling.csv`.
   - To add a new system configuration:
     - Click `Add Row`, enter the details in the new window, and click `Save`.
   - To edit an existing system configuration:
     - Select a row, click `Edit Selected`, modify the details in the new window, and click `Save`.
   - To delete a system configuration:
     - Select a row or multiple rows and click `Delete Selected`.

### Changing System Resolutions
- Use the `System` dropdown to select a gaming system.
- The width and height fields will automatically populate based on the selected system.
- These values can be manually adjusted for creating custom-sized overlays.

### Additional Features
- Use the `Backspace` key to delete selected image files.
- Press `r` to refresh the list of images.

By following these steps, you can easily create custom overlays and manage system configurations for your retro gaming setup.

<!-- GETTING STARTED -->
## Standalone APP

Install pyintaller
```
pip install pyinstaller
```
Generate the standalone app
```
pyinstaller --windowed --onefile your_script_name.py
```

## Create DMG(MacOS)

#### Step 1: Create a New Folder for DMG Contents

##### 1. Create a New Folder:
+ Create a new folder on your desktop or in another convenient location. 
+ This folder will hold the contents of your * . dmg file.
+ Name it something like 'DMGContents" or similar.

##### 2. Copy Your App and Applications Shortcut:
+ Copy your "YourApp.app* file into this new folder.
+ Open a new Finder window and go to the /Applications' folder.
+ Drag the Applications folder into your 'DMGContents" folder while holding down the Cmd and 'Alt keys. This will create an alias (shortcut) to the Applications folder in your 'DMContents" folder.

#### Step 2: Create the DMG File
+ Now, use Disk Utility or the 'hdiutil command to create your . dm file from the "DMGContents" folder.
+ Using Disk Utility:

Follow the steps previously described but select the DMGContents* folder instead of just the app.
+ Using Terminal with hdiutil:
+ Use the hdiutil' command like before, but point it to your DMContents" folder.

For example:
```
hdiutil create -volname "YourApp" -srcfolder /path/to/YourApp.app -ov -format UDZO YourApp.dmg
```

#### Step 3: Customize the DMG Appearance (Optional)
+ To make the . dmg file look more professional, you can customize its appearance:

+ Mount the DMG: Double-click the " . dmg" file to mount it.
+ Open the Mounted Volume: Open the mounted volume in Finder.
+ Arrange Icons: Arrange the app and the Applications shortcut in a way that encourages the user to drag the app into the Applications folder.
+ You can add text instructions or use a background image to make this more intuitive.
+ Set Icon Sizes and View Options:

Set the icon size and the view options as you prefer (e.g., using 'View Show View Options' in Finder).

+ You can make these view options default for all who open the dm by clicking
+ Use as Defaults" at the bottom of the view options window.
+ Eject and Test:
+ After arranging everything, eject the dm (by dragging the mounted volume to the Trash or right-clicking and selecting 'Eject *) and then remount it to ensure your changes are saved.

#### Step 4: Distribute the DMG File
Once you're satisfied with the appearance and functionality, your * . dm file is ready for distribution.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

<a href="https://www.python.org">
<img src="https://github.com/gelndjj/Nostalgia_Frames/blob/main/resources/py_icon.png" alt="Icon" width="32" height="32">
</a>
<p align="right">(<a href="#readme-top">back to top</a>)</p>
    

<!-- LICENSE -->
## License

Distributed under the GNU GENERAL PUBLIC LICENSE. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact


[LinkedIn](https://www.linkedin.com/in/jonathanduthil/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 