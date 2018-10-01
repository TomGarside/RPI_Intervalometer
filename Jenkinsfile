node{

    sh "rm -r RPI_Intervalometer"
    sh "git clone https://github.com/TomGarside/RPI_Intervalometer.git"
    sh "pip3 freeze"
    sh "pip3 install gphoto2cffi, RPI.GPIO, RPLCD"
    sh "python3 RPI_Intervalometer/timelapse.py"

}