# Mapt

Shape file sharing application, testing out RMWC as a component framework

# Add a backend dependency

As the development environment is containerised the Docker image needs to rebuilt after running
pip install in the container. To add a new dependency use the command:

```
make pip-install <MY_PACKAGE>
```
