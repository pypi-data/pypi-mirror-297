import time

from spikewrap.pipeline.full_pipeline import run_full_pipeline


config_name = "test_default"


def get_sessions_and_runs(mtd):
    sessions_and_runs = {
                         s.session_path_derivatives.stem: [
                            x.parent.stem for x in list(s.session_path_raw.rglob("*.ap.bin"))
        ]

        for s in mtd.sessions
    }
    if len(sessions_and_runs.values()) == 0:
        raise ValueError(f"no sessions and/or runs found: {sessions_and_runs}")
    return sessions_and_runs


def run_full_sorting_pipeline_on_mouse(mtd, sorter="kilosort2_5"):
    sessions_and_runs = get_sessions_and_runs(mtd)
    base_path = mtd.rawdata_directory.parent
    t = time.time()
    print("using new edits")

    for session, runs in sessions_and_runs.items():
        single_session_dict = {session: runs}
        run_full_pipeline(
            base_path=base_path,
            sub_name=mtd.mouse_id,
            sessions_and_runs=single_session_dict,
            data_format='spikeglx',
            config_name=config_name,
            sorter=sorter,
            concat_sessions_for_sorting=False,
            concat_runs_for_sorting=False,
            existing_preprocessed_data="skip_if_exists",  # this is kind of confusing...
            existing_sorting_output="skip_if_exists",
            overwrite_postprocessing=True,
            delete_intermediate_files=(),
            slurm_batch=True,
            save_preprocessing_chunk_size=12000,
        )

        print(f"TOOK {time.time() - t}")
