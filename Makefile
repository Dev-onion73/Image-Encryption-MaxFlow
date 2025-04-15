CXX = g++
CXXFLAGS = `pkg-config --cflags --libs opencv4`
SRC_DIR = cryptlib

ENCRYPT_SRC = $(SRC_DIR)/encrypt.cpp
DECRYPT_SRC = $(SRC_DIR)/decrypt.cpp
ENCRYPT_BIN = $(SRC_DIR)/encrypt
DECRYPT_BIN = $(SRC_DIR)/decrypt

all: $(ENCRYPT_BIN) $(DECRYPT_BIN)

$(ENCRYPT_BIN): $(ENCRYPT_SRC)
	$(CXX) $< -o $@ $(CXXFLAGS)

$(DECRYPT_BIN): $(DECRYPT_SRC)
	$(CXX) $< -o $@ $(CXXFLAGS)

clean:
	rm -f $(ENCRYPT_BIN) $(DECRYPT_BIN)

.PHONY: all clean
