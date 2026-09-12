#ifndef LIDAR_HPP
#define LIDAR_HPP

#include <string>

class Lidar {
private:
    std::string name;
    int* health;

public:
    // 1. Default Constructor
    Lidar();

    // 2. Parameterized Constructor
    Lidar(std::string n, int h);

    // 3. Copy Constructor
    Lidar(const Lidar& other);

    // 4. Move Constructor
    Lidar(Lidar&& other) noexcept;

    // Destructor
    ~Lidar();

    // Utility display function
    // void print_status() const;
};

#endif // PLAYER_HPP
