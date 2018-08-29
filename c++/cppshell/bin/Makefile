CC= g++
CFLAGS= -Wall -std=c++11

# Directory paths for *.c and *.h files
source= ../src/source/
headers= ../src/headers/

# All object files needed by cppshell
objects= helper.o built_ins.o

# Name of executable to build and its source file
TARGET= cppshell

# Command used to compile executable
build_command= $(CC) $(CFLAGS) -I $(headers) $(objects) $(source)$(TARGET).cpp -o $(TARGET)

# Add debugging information to debug target
default: build
debug: CFLAGS += -g
debug: build

build: $(objects)
	$(build_command)
	-rm -f *.o
	-rm -f *.gch

buildAll: $(objects)
	$(build_command)

$(objects): %.o : $(source)%.cpp
	$(CC) $(CFLAGS) -I $(headers) -c $< -o $@

clean:
	-rm -f *.o
	-rm -f *.gch

cleanAll:
	-rm -f *.o
	-rm -f *.gch
	-rm -f $(TARGET)

