# Electronic Music Accompaniment Generation

## Team Members:

Matthew Avallone and Anish Malhotra

## Summary:

The goal of this project is to develop a deep learning platform that takes a melody for a song and generates an accompaniment for it of different instrument classes (i.e. strings, brass, percussion etc.). The problem is viewed as an instance of neural machine translation, where the melody gets passed through an LSTM encoder-decoder neural network that encodes an input matrix of notes and decodes an output matrix of notes. Each instrument class has its own trained model, due to the unique structure and format of their parts.

The songs are stored as MIDI files, with each containing its own "pianoroll" matrix of notes (time_step x num_of_notes). The pianorolls are preprocessed into smaller phrases and are used to train the networks. Training is done using Google Colab and Kaggle, since we have a limited budget and their compute resources are free. The output accompaniment for each instrument class is post processed back into a song.

This repo contains Python scripts and Jupyter notebooks. The post processing notebook will be ported to Python script soon.

## Special Libraries Used:

* pypianoroll
* pretty_midi
* suffix_tree

## Training Data (full-length MIDI songs):

https://drive.google.com/drive/folders/1fLKu7bRD4fwAui_uAl-8moguRwuV-DMR?usp=sharing

## Test Data:

Check out test songs folder

## Coming Soon:

* Demos
* Research Paper
* Website
