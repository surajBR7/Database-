import subprocess

def main():
    # Run the query runner
    subprocess.run(['python', 'queryandtime.py'])
    #run the plot file
    subprocess.run(['python', 'plot.py'])

if __name__ == "__main__":
    main()
