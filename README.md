# Cloudbox

<p align="center">
  <img src="https://raw.githubusercontent.com/Cloudbox/assets/master/images/readme/Cloudbox-logo_dark.png" width="600">
</p>

<p align="center">
  <a href="https://cloudbox.works">
    <img src="https://img.shields.io/badge/Website-https%3A%2F%2Fcloudbox.works-blue.svg?style=for-the-badge&colorB=177DC1&label=website" alt="Website">
  </a>
  <a href="https://discord.io/cloudbox">
    <img src="https://img.shields.io/badge/Discord-gray.svg?style=for-the-badge" alt="Discord">
  </a>
  <a href="https://reddit.com/r/Cloudbox">
    <img src="https://img.shields.io/badge/Reddit-gray.svg?style=for-the-badge" alt="Reddit">
  </a>
  <a href="LICENSE.md">
    <img src="https://img.shields.io/badge/License-GPL%203-blue.svg?style=for-the-badge&colorB=177DC1&label=license" alt="License">
  </a>
</p>

Cloudbox is an Ansible-based solution for rapidly deploying a Docker containerized cloud media server. It provides a simple and automated way to set up a powerful media server on your own hardware or a rented server.

## Features

Cloudbox comes with a wide range of applications for managing and streaming your media content. Some of the featured applications include:

- **Media Servers**: Plex, Emby
- **Download Clients**: NZBGet, ruTorrent, SABnzbd
- **Indexers and Trackers**: Jackett, NZBHydra2
- **Automation**: Sonarr, Radarr, Lidarr, Bazarr
- **Management and Monitoring**: Tautulli (PlexPy), Portainer, Netdata
- **And many more...**

For a full list of available applications, see the `cloudbox.yml` file.

## Prerequisites

To use Cloudbox, you will need the following:

- A server running **Ubuntu Server 18.04 (Bionic Beaver)**. Other Debian-based distributions may work but are not officially supported.
- An **x64 (64-bit)** processor.
- **Ansible** installed on your local machine or on the server itself.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Cloudbox/Cloudbox.git
    cd Cloudbox
    ```

2.  **Create your configuration files**:
    Cloudbox is configured using YAML files. You will need to create your own configuration files by copying the provided default files.

    -   Copy `defaults/accounts.yml.default` to `accounts.yml`.
    -   Copy `defaults/settings.yml.default` to `settings.yml`.

    You can also copy `defaults/adv_settings.yml.default` to `adv_settings.yml` and `defaults/backup_config.yml.default` to `backup_config.yml` for advanced configuration and backup settings.

3.  **Customize your configuration**:
    Edit the `accounts.yml` and `settings.yml` files to match your needs. At a minimum, you should change the default username and password in `accounts.yml`.

4.  **Install Ansible roles**:
    Cloudbox uses Ansible Galaxy to manage its role dependencies. Install the required roles by running:
    ```bash
    ansible-galaxy install -r requirements.yml
    ```
    _Note: If `requirements.yml` does not exist, this step might not be necessary._

5.  **Run the Ansible playbook**:
    Execute the following command to start the Cloudbox installation:
    ```bash
    ansible-playbook cloudbox.yml
    ```
    This will install and configure all the applications specified in the playbook. You can use tags to install specific parts of the Cloudbox stack. For example, to only install Plex, you can run:
    ```bash
    ansible-playbook cloudbox.yml --tags plex
    ```

## Configuration

Cloudbox is highly configurable. The main configuration files are:

-   **`accounts.yml`**: Used to configure usernames, passwords, API keys, and other sensitive information.
-   **`settings.yml`**: Used to configure general settings for your Cloudbox installation, such as download paths and application-specific settings.
-   **`adv_settings.yml`**: For advanced settings that are not commonly changed.
-   **`backup_config.yml`**: To configure backup settings.

These files are located in the root directory of the Cloudbox project. You must create them by copying the `.default` files from the `defaults/` directory.

## Usage

Once the Ansible playbook has finished running, your Cloudbox server will be up and running. The various applications will be available at the domain you configured in `accounts.yml`. For example, if your domain is `example.com`, you will be able to access Plex at `http://plex.example.com`.

A web portal like Organizr or Heimdall is usually installed to provide a single entry point to all your applications.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to the project.

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE.md](LICENSE.md) file for details.
