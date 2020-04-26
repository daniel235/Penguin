# Penguin
Tool to extract and classify PseudoUridine signals from fast5 files

## Tool workflow
The penguin tool needs as input a fast5 path and if you don't provide a sam file you have to provide a reference genome to align to so the tool can create the sam file.  If no bed file is provided a default one is included and will be used.
The tool will then id all fast5 files and create coordinate file with ids of files that are modified.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To use guppy basecaller you have to be a community member.  

### Installing

First run the install.sh file to get all required files to run the program.

```
./install.sh
```

## Running the tool

```
-i fast5 path(required)
-s samfile
-b bedfile(Default if not included)
-ref reference Genome (Default if not included)
```

## Example

```
python main.py -i ~/fast5_directory/ -s ~/sam_directory/my_sam_file.sam -b ~/bed_directory/my_bed_file.bed
```


## Built With

* [Tensorflow](https://www.tensorflow.org/) - Used to generate ml models

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Daniel Acevedo** - *Initial work* - [Daniel235](https://github.com/daniel235)
* **Doaa Salem** - Models - [hsdoaa](https://github.com/hsdoaa)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Falcon
