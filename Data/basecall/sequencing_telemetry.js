[
    {
        "aggregation": "segment",
        "analysis_id": "cbf7af67-ca9c-4056-81d1-78b8cc4aed74",
        "basecall_1d": {
            "exit_status_dist": {
                "fail:qscore_filter": 1,
                "pass": 21
            },
            "qscore_dist_temp": [
                {
                    "count": 1,
                    "mean_qscore": 6.0
                },
                {
                    "count": 3,
                    "mean_qscore": 8.0
                },
                {
                    "count": 1,
                    "mean_qscore": 8.5
                },
                {
                    "count": 5,
                    "mean_qscore": 9.0
                },
                {
                    "count": 2,
                    "mean_qscore": 9.5
                },
                {
                    "count": 2,
                    "mean_qscore": 10.0
                },
                {
                    "count": 2,
                    "mean_qscore": 10.5
                },
                {
                    "count": 1,
                    "mean_qscore": 11.0
                },
                {
                    "count": 4,
                    "mean_qscore": 11.5
                },
                {
                    "count": 1,
                    "mean_qscore": 12.5
                }
            ],
            "qscore_sum_temp": {
                "count": 22,
                "mean": 9.94408321380615,
                "sum": 218.769836425781
            },
            "read_len_events_sum_temp": 55320,
            "seq_len_bases_dist_temp": [
                {
                    "count": 22,
                    "length": 0.0
                }
            ],
            "seq_len_bases_sum_temp": 22,
            "seq_len_events_dist_temp": [
                {
                    "count": 7,
                    "length": 1000.0
                },
                {
                    "count": 9,
                    "length": 2000.0
                },
                {
                    "count": 6,
                    "length": 3000.0
                }
            ],
            "speed_bases_per_second_dist_temp": [
                {
                    "count": 22,
                    "speed": 1.0
                }
            ],
            "strand_median_pa": {
                "count": 22,
                "mean": 95.1336364746094,
                "sum": 2092.93994140625
            },
            "strand_sd_pa": {
                "count": 22,
                "mean": 13.85422706604,
                "sum": 304.792999267578
            }
        },
        "channel_count": 22,
        "context_tags": {
            "experiment_duration_set": "2880",
            "experiment_type": "rna",
            "fast5_output_fastq_in_hdf": "1",
            "fast5_raw": "1",
            "fast5_reads_per_folder": "4000",
            "fastq_enabled": "1",
            "fastq_reads_per_file": "4000",
            "filename": "in_bio_sl351j_20180705_fah87710_mn27375_sequencing_run_hela_070518_26999",
            "flowcell_type": "flo-min106",
            "kit_classification": "none",
            "local_basecalling": "1",
            "local_bc_comp_model": "",
            "local_bc_temp_model": "template_r9.4_70bps_5mer_rna_raw.jsn",
            "sample_frequency": "3012",
            "sequencing_kit": "sqk-rna001",
            "user_filename_input": "hela_070518"
        },
        "latest_run_time": 75.8944244384766,
        "levels_sums": {
            "count": 22,
            "mean": 224.013412475586,
            "open_pore_level_sum": 4928.294921875
        },
        "opts": {
            "adapter_pt_range_scale": "5.200000",
            "allow_inferior_barcodes": "0",
            "arrangements_files": "",
            "as_cpu_threads_per_scaler": "2",
            "as_gpu_runners_per_device": "2",
            "as_model_file": "",
            "as_num_scalers": "1",
            "as_reads_per_runner": "32",
            "barcode_kits": "",
            "barcoding_config_file": "configuration.cfg",
            "builtin_scripts": "1",
            "calib_detect": "0",
            "calib_max_sequence_length": "1550",
            "calib_min_coverage": "0.600000",
            "calib_min_sequence_length": "1100",
            "calib_reference": "YHR174W.fasta",
            "chunk_size": "2000",
            "chunks_per_caller": "10000",
            "chunks_per_runner": "512",
            "client_id": "-1",
            "compress_fastq": "0",
            "cpu_threads_per_caller": "4",
            "detect_mid_strand_barcodes": "0",
            "device": "",
            "disable_events": "0",
            "disable_pings": "0",
            "dmean_threshold": "10.000000",
            "dmean_win_size": "400",
            "end_gap1": "40",
            "end_gap2": "40",
            "extend_gap1": "40",
            "extend_gap2": "160",
            "fast5_out": "0",
            "flowcell": "",
            "front_window_size": "150",
            "gpu_runners_per_device": "4",
            "high_priority_threshold": "10",
            "input_file_list": "",
            "jump_threshold": "2.000000",
            "kernel_path": "",
            "kit": "",
            "log_speed_frequency": "0",
            "max_block_size": "50000",
            "max_search_len": "15000",
            "medium_priority_threshold": "4",
            "min_qscore": "7.000000",
            "min_score": "60.000000",
            "min_score_mid_barcodes": "60.000000",
            "min_score_rear_override": "60.000000",
            "model_file": "template_rna_r9.4.1_70bps_hac.jsn",
            "nested_output_folder": "0",
            "num_barcode_threads": "4",
            "num_barcoding_buffers": "96",
            "num_callers": "1",
            "num_extra_bases_trim": "0",
            "open_gap1": "40",
            "open_gap2": "160",
            "overlap": "50",
            "override_scaling": "0",
            "ping_segment_duration": "60",
            "ping_url": "https://ping.oxfordnanoportal.com/basecall",
            "port": "",
            "post_out": "0",
            "print_workflows": "0",
            "progress_stats_frequency": "-1.000000",
            "pt_median_offset": "2.500000",
            "pt_minimum_read_start_index": "30",
            "pt_required_adapter_drop": "30.000000",
            "pt_scaling": "0",
            "qscore_filtering": "0",
            "qscore_offset": "0.420000",
            "qscore_scale": "0.880000",
            "quiet": "0",
            "read_batch_size": "4000",
            "read_id_list": "",
            "rear_window_size": "150",
            "records_per_fastq": "4000",
            "recursive": "0",
            "require_barcodes_both_ends": "0",
            "resume": "0",
            "reverse_sequence": "1",
            "scaling_mad": "1.000000",
            "scaling_med": "0.000000",
            "score_matrix_filename": "",
            "start_gap1": "40",
            "start_gap2": "40",
            "stay_penalty": "1.000000",
            "temp_bias": "1.000000",
            "temp_weight": "1.000000",
            "trace_categories_logs": "",
            "trim_barcodes": "0",
            "trim_min_events": "100",
            "trim_strategy": "rna",
            "trim_threshold": "5.000000",
            "u_substitution": "1",
            "verbose_logs": "0"
        },
        "read_count": 22,
        "reads_per_channel_dist": [
            {
                "channel": 32,
                "count": 1
            },
            {
                "channel": 67,
                "count": 1
            },
            {
                "channel": 132,
                "count": 1
            },
            {
                "channel": 142,
                "count": 1
            },
            {
                "channel": 153,
                "count": 1
            },
            {
                "channel": 157,
                "count": 1
            },
            {
                "channel": 169,
                "count": 1
            },
            {
                "channel": 219,
                "count": 1
            },
            {
                "channel": 230,
                "count": 1
            },
            {
                "channel": 234,
                "count": 1
            },
            {
                "channel": 251,
                "count": 1
            },
            {
                "channel": 269,
                "count": 1
            },
            {
                "channel": 272,
                "count": 1
            },
            {
                "channel": 284,
                "count": 1
            },
            {
                "channel": 310,
                "count": 1
            },
            {
                "channel": 330,
                "count": 1
            },
            {
                "channel": 331,
                "count": 1
            },
            {
                "channel": 360,
                "count": 1
            },
            {
                "channel": 361,
                "count": 1
            },
            {
                "channel": 465,
                "count": 1
            },
            {
                "channel": 466,
                "count": 1
            },
            {
                "channel": 489,
                "count": 1
            }
        ],
        "run_id": "85331a9859f4761d810f4a1e7b497e769c1e262c",
        "segment_duration": 60,
        "segment_number": 1,
        "segment_type": "guppy-acquisition",
        "software": {
            "analysis": "1d_basecalling",
            "name": "guppy-basecalling",
            "version": "3.5.2+5b7a51b"
        },
        "tracking_id": {
            "asic_id": "4178240229",
            "asic_id_eeprom": "2370264",
            "asic_temp": "24.667381",
            "asic_version": "IA02C",
            "auto_update": "0",
            "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/",
            "bream_is_standard": "0",
            "device_id": "MN27375",
            "device_type": "minion",
            "exp_script_name": "bdb0a03094684b26c87d3e01300dc343c5387145-9ac881a19342ff7f47b5c217536b3a50e6b51e07",
            "exp_script_purpose": "sequencing_run",
            "exp_start_time": "2018-07-05T22:27:01Z",
            "flow_cell_id": "FAH87710",
            "heatsink_temp": "34.257813",
            "hostname": "IN-BIO-SL351J",
            "installation_type": "nc",
            "local_firmware_file": "1",
            "msg_id": "9b612374-a70b-4e20-b073-0156fa0ed4b0",
            "operating_system": "Windows 10.0",
            "protocol_run_id": "7991e75a-07b6-4b86-99cd-389ef124652f",
            "protocols_version": "1.13.0.13",
            "run_id": "85331a9859f4761d810f4a1e7b497e769c1e262c",
            "sample_id": "hela_070518",
            "time_stamp": "2020-04-08T05:24:30Z",
            "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3",
            "version": "1.13.1"
        }
    },
    {
        "aggregation": "cumulative",
        "analysis_id": "cbf7af67-ca9c-4056-81d1-78b8cc4aed74",
        "basecall_1d": {
            "exit_status_dist": {
                "fail:qscore_filter": 1,
                "pass": 21
            },
            "qscore_dist_temp": [
                {
                    "count": 1,
                    "mean_qscore": 6.0
                },
                {
                    "count": 3,
                    "mean_qscore": 8.0
                },
                {
                    "count": 1,
                    "mean_qscore": 8.5
                },
                {
                    "count": 5,
                    "mean_qscore": 9.0
                },
                {
                    "count": 2,
                    "mean_qscore": 9.5
                },
                {
                    "count": 2,
                    "mean_qscore": 10.0
                },
                {
                    "count": 2,
                    "mean_qscore": 10.5
                },
                {
                    "count": 1,
                    "mean_qscore": 11.0
                },
                {
                    "count": 4,
                    "mean_qscore": 11.5
                },
                {
                    "count": 1,
                    "mean_qscore": 12.5
                }
            ],
            "qscore_sum_temp": {
                "count": 22,
                "mean": 9.94408321380615,
                "sum": 218.769836425781
            },
            "read_len_events_sum_temp": 55320,
            "seq_len_bases_dist_temp": [
                {
                    "count": 22,
                    "length": 0.0
                }
            ],
            "seq_len_bases_sum_temp": 22,
            "seq_len_events_dist_temp": [
                {
                    "count": 7,
                    "length": 1000.0
                },
                {
                    "count": 9,
                    "length": 2000.0
                },
                {
                    "count": 6,
                    "length": 3000.0
                }
            ],
            "speed_bases_per_second_dist_temp": [
                {
                    "count": 22,
                    "speed": 1.0
                }
            ],
            "strand_median_pa": {
                "count": 22,
                "mean": 95.1336364746094,
                "sum": 2092.93994140625
            },
            "strand_sd_pa": {
                "count": 22,
                "mean": 13.85422706604,
                "sum": 304.792999267578
            }
        },
        "channel_count": 22,
        "context_tags": {
            "experiment_duration_set": "2880",
            "experiment_type": "rna",
            "fast5_output_fastq_in_hdf": "1",
            "fast5_raw": "1",
            "fast5_reads_per_folder": "4000",
            "fastq_enabled": "1",
            "fastq_reads_per_file": "4000",
            "filename": "in_bio_sl351j_20180705_fah87710_mn27375_sequencing_run_hela_070518_26999",
            "flowcell_type": "flo-min106",
            "kit_classification": "none",
            "local_basecalling": "1",
            "local_bc_comp_model": "",
            "local_bc_temp_model": "template_r9.4_70bps_5mer_rna_raw.jsn",
            "sample_frequency": "3012",
            "sequencing_kit": "sqk-rna001",
            "user_filename_input": "hela_070518"
        },
        "latest_run_time": 75.8944244384766,
        "levels_sums": {
            "count": 22,
            "mean": 224.013412475586,
            "open_pore_level_sum": 4928.294921875
        },
        "opts": {
            "adapter_pt_range_scale": "5.200000",
            "allow_inferior_barcodes": "0",
            "arrangements_files": "",
            "as_cpu_threads_per_scaler": "2",
            "as_gpu_runners_per_device": "2",
            "as_model_file": "",
            "as_num_scalers": "1",
            "as_reads_per_runner": "32",
            "barcode_kits": "",
            "barcoding_config_file": "configuration.cfg",
            "builtin_scripts": "1",
            "calib_detect": "0",
            "calib_max_sequence_length": "1550",
            "calib_min_coverage": "0.600000",
            "calib_min_sequence_length": "1100",
            "calib_reference": "YHR174W.fasta",
            "chunk_size": "2000",
            "chunks_per_caller": "10000",
            "chunks_per_runner": "512",
            "client_id": "-1",
            "compress_fastq": "0",
            "cpu_threads_per_caller": "4",
            "detect_mid_strand_barcodes": "0",
            "device": "",
            "disable_events": "0",
            "disable_pings": "0",
            "dmean_threshold": "10.000000",
            "dmean_win_size": "400",
            "end_gap1": "40",
            "end_gap2": "40",
            "extend_gap1": "40",
            "extend_gap2": "160",
            "fast5_out": "0",
            "flowcell": "",
            "front_window_size": "150",
            "gpu_runners_per_device": "4",
            "high_priority_threshold": "10",
            "input_file_list": "",
            "jump_threshold": "2.000000",
            "kernel_path": "",
            "kit": "",
            "log_speed_frequency": "0",
            "max_block_size": "50000",
            "max_search_len": "15000",
            "medium_priority_threshold": "4",
            "min_qscore": "7.000000",
            "min_score": "60.000000",
            "min_score_mid_barcodes": "60.000000",
            "min_score_rear_override": "60.000000",
            "model_file": "template_rna_r9.4.1_70bps_hac.jsn",
            "nested_output_folder": "0",
            "num_barcode_threads": "4",
            "num_barcoding_buffers": "96",
            "num_callers": "1",
            "num_extra_bases_trim": "0",
            "open_gap1": "40",
            "open_gap2": "160",
            "overlap": "50",
            "override_scaling": "0",
            "ping_segment_duration": "60",
            "ping_url": "https://ping.oxfordnanoportal.com/basecall",
            "port": "",
            "post_out": "0",
            "print_workflows": "0",
            "progress_stats_frequency": "-1.000000",
            "pt_median_offset": "2.500000",
            "pt_minimum_read_start_index": "30",
            "pt_required_adapter_drop": "30.000000",
            "pt_scaling": "0",
            "qscore_filtering": "0",
            "qscore_offset": "0.420000",
            "qscore_scale": "0.880000",
            "quiet": "0",
            "read_batch_size": "4000",
            "read_id_list": "",
            "rear_window_size": "150",
            "records_per_fastq": "4000",
            "recursive": "0",
            "require_barcodes_both_ends": "0",
            "resume": "0",
            "reverse_sequence": "1",
            "scaling_mad": "1.000000",
            "scaling_med": "0.000000",
            "score_matrix_filename": "",
            "start_gap1": "40",
            "start_gap2": "40",
            "stay_penalty": "1.000000",
            "temp_bias": "1.000000",
            "temp_weight": "1.000000",
            "trace_categories_logs": "",
            "trim_barcodes": "0",
            "trim_min_events": "100",
            "trim_strategy": "rna",
            "trim_threshold": "5.000000",
            "u_substitution": "1",
            "verbose_logs": "0"
        },
        "read_count": 22,
        "reads_per_channel_dist": [
            {
                "channel": 32,
                "count": 1
            },
            {
                "channel": 67,
                "count": 1
            },
            {
                "channel": 132,
                "count": 1
            },
            {
                "channel": 142,
                "count": 1
            },
            {
                "channel": 153,
                "count": 1
            },
            {
                "channel": 157,
                "count": 1
            },
            {
                "channel": 169,
                "count": 1
            },
            {
                "channel": 219,
                "count": 1
            },
            {
                "channel": 230,
                "count": 1
            },
            {
                "channel": 234,
                "count": 1
            },
            {
                "channel": 251,
                "count": 1
            },
            {
                "channel": 269,
                "count": 1
            },
            {
                "channel": 272,
                "count": 1
            },
            {
                "channel": 284,
                "count": 1
            },
            {
                "channel": 310,
                "count": 1
            },
            {
                "channel": 330,
                "count": 1
            },
            {
                "channel": 331,
                "count": 1
            },
            {
                "channel": 360,
                "count": 1
            },
            {
                "channel": 361,
                "count": 1
            },
            {
                "channel": 465,
                "count": 1
            },
            {
                "channel": 466,
                "count": 1
            },
            {
                "channel": 489,
                "count": 1
            }
        ],
        "run_id": "85331a9859f4761d810f4a1e7b497e769c1e262c",
        "segment_duration": 60,
        "segment_number": 1,
        "segment_type": "guppy-acquisition",
        "software": {
            "analysis": "1d_basecalling",
            "name": "guppy-basecalling",
            "version": "3.5.2+5b7a51b"
        },
        "tracking_id": {
            "asic_id": "4178240229",
            "asic_id_eeprom": "2370264",
            "asic_temp": "24.667381",
            "asic_version": "IA02C",
            "auto_update": "0",
            "auto_update_source": "https://mirror.oxfordnanoportal.com/software/MinKNOW/",
            "bream_is_standard": "0",
            "device_id": "MN27375",
            "device_type": "minion",
            "exp_script_name": "bdb0a03094684b26c87d3e01300dc343c5387145-9ac881a19342ff7f47b5c217536b3a50e6b51e07",
            "exp_script_purpose": "sequencing_run",
            "exp_start_time": "2018-07-05T22:27:01Z",
            "flow_cell_id": "FAH87710",
            "heatsink_temp": "34.257813",
            "hostname": "IN-BIO-SL351J",
            "installation_type": "nc",
            "local_firmware_file": "1",
            "msg_id": "5498f9c7-a7b9-4869-8b5f-8ff2b6fa8b20",
            "operating_system": "Windows 10.0",
            "protocol_run_id": "7991e75a-07b6-4b86-99cd-389ef124652f",
            "protocols_version": "1.13.0.13",
            "run_id": "85331a9859f4761d810f4a1e7b497e769c1e262c",
            "sample_id": "hela_070518",
            "time_stamp": "2020-04-08T05:24:30Z",
            "usb_config": "firm_1.2.3_ware#rbt_4.5.6_rbt#ctrl#USB3",
            "version": "1.13.1"
        }
    }
]