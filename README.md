# File-Change-Monitoring-and-Logging-System
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%204.0-blue.svg)](https://www.python.org/)

## Table of Contents

- Overview
- Project Description
- Features
- System Operation
- Database Schema
- Usage
- Future Enhancements
- References
- Acknowledgments
  
## Overview

Welcome to the **File Change Monitoring and Logging System** repository! This project is designed to address the critical need for monitoring and logging changes in files within a Windows environment. It enables real-time detection of file modifications, additions, and deletions and stores these changes in a secure database.

## Project Description

This project aims to provide a robust and comprehensive solution for monitoring and logging file changes within a Windows operating system. Whether it's detecting unauthorized access, tracking document revisions, or ensuring data integrity, our system offers a reliable means of file change management.

## Features

- Real-time monitoring of file changes.
- Automatic backup of modified files.
- Database storage of all file changes.
- Secure, unique change logging with no data redundancy.
- Compatibility with Windows OS.

## System Operation

Our system operates as follows:

1. Monitors specified directories for file changes.
2. Creates backups of modified files.
3. Logs all file changes in a secure database.

## Database Schema

The project employs a two-table database schema:

### 1. `backup_paths` Table

- Stores mappings between original files and their backup copies.
  

### 2. `differences` Table

- Logs all unique file changes, preventing data duplication.
- Records operation type (Insert, Update, Delete) and affected lines.

## Usage

To use the File Change Monitoring and Logging System:

1. Clone the repository to your local machine.
2. Install the required Python libraries.
3. Configure the database connection.
4. Run the main script to initiate monitoring.

## Future Enhancements

We envision several enhancements for the system:

- Integration with Windows Task Scheduler for scheduling monitoring tasks.
- Cross-platform compatibility for Linux and other OS.
- Enhanced reporting and visualization tools.
- User-friendly GUI for easier configuration.

## References

This project leverages various open-source technologies, including Python, MySQL and difflib. I acknowledge their contributions to the project's success.

## Acknowledgments

I extend my gratitude to my mentor, Mr. Praveen Kumar and System Department of South Eastern Coalfields Limited (HQ)  for their invaluable support and insights throughout this project.
