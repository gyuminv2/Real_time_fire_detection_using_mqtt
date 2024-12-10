#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

int main() {
    float temperature;
    srand(time(0));

    const char *pipe_name = "/tmp/temp_pipe";
    if (mkfifo(pipe_name, 0666) == -1) {
        perror("Failed to create named pipe");
        return 1;
    }

    FILE *pipe = fopen(pipe_name, "w");
    if (!pipe) {
        perror("Failed to open pipe");
        return 1;
    }

    while (1) {
        temperature = 10.0 + (rand() % 910) / 10.0;
        fprintf(pipe, "%.2f\n", temperature);
        fflush(pipe);
        printf("Generated Temperature: %.2f°C\n", temperature);
        sleep(5);
    }

    fclose(pipe);
    return 0;
}