#include <stdio.h>
#include <fdeep/fdeep.hpp>

#define BUFLEN 1024
#define IMG_CH 3

fdeep::tensor5 ppm_to_tensor5(const char *filename, fdeep::float_type low = 0.0f, fdeep::float_type high = 1.0f)
{
    if (strstr(filename, ".ppm") == NULL) exit(1);
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) exit(1);
    char buf[BUFLEN];

    int idx = 0;
    int width = -1;
    int height = -1;
    while (idx<3 && (fgets(buf, BUFLEN, fp) != NULL)) {
        if (buf[0] == '#') continue;
        switch(idx++) {
        case 0:
            if (buf[1] != '6') exit(1);
            break;
        case 1:
            sscanf(buf, "%d %d", &width, &height);
            break;
        case 2:
            int level;
            sscanf(buf, "%d", &level);
            if (level != 255) exit(1);
            break;
        }
    }

    unsigned char ch;
    std::vector<unsigned char> pixels;
    pixels.reserve(height * width * IMG_CH);
    for (int y=0; y<height; y++) {
        for (int x=0; x<width; x++) {
            for (int c=0; c<IMG_CH; c++) {
                if ((ch = fgetc(fp)) == EOF) exit(1);
                pixels.push_back(ch);
            }
        }
    }

    return fdeep::tensor5_from_bytes(pixels.data(), height, width, IMG_CH, low, high);
}


int main(int argc, char *argv[])
{
    if (argc < 3) return 1;

    const auto model = fdeep::load_model(argv[1]);
    for (int i=2; i<argc; i++) {
        const auto input = ppm_to_tensor5(argv[i], 0.0f, 1.0f);
        const auto result = model.predict_class({input});
        printf("predictresult%s:", argv[i]);
        std::cout << result << std::endl;
    }

    return 0;
}
