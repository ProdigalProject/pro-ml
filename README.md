# Prodigal Project
Prodigal is an open-source web application to provide stock prediction values derived from linear regression models with the goal of providing users with useful insights that can generate profits.

## Team Members
- Balaji Pandurangan Baskaran
- Wonwoo Seo
- Sean Lin
- Htut Khine Win
- Jamie Paterson
- Gabrielle Chen

## pro-ml
Back-end (API) codes for the project. Provides history data of company, or runs prediction experiment on request.

### API endpoints
|REST  | ENDPOINT     | 
|------|--------------|
|GET   | /stocks/     |
|GET   | /stocks/[ticker] | 
|GET   | /stocks/[ticker]/runexpr |
|GET   | /stocks/update |
|GET   | /stocks/[ticker]/update |

## Link to Web Application
https://prodigal-beta.azurewebsites.net

## Doxygen Instructions
1. [Download doxygen binaries for your environment.](http://www.stack.nl/~dimitri/doxygen/download.html)
    1. If on Linux / macOS, you can also use following commands to get doxygen binaries:
    2. ```wget http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.2.linux.bin.tar.gz```
2. Place doxygen binaries at root of the project.
3. Run ```doxygen Doxygen-Prodigal-ml``` command at root of the project from bash, terminal or command prompt.

## Docker Deployment Instructions
1. Run Docker container.
2. Run ```docker pull hwin16/prodigal-ml:v1.0.7```
3. Run ```docker run -p 8000:8000 hwin16/prodigal-ml:v1.0.7```

## Documentations
[Documentation pdf](prodigal_documentation.pdf)