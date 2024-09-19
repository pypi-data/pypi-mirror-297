import time

from spikewrap.pipeline.full_pipeline import run_full_pipeline


config_name = "test_default"


def run_full_sorting_pipeline_on_mouse(mtd, sorter="kilosort2_5"):
    base_path = mtd.root.parent
    sessions_and_runs = {
        # s.session_path_derivatives.stem: [
        #     x.stem for x in list(s.session_path_raw.rglob("*run*"))
        # ]
        s.session_path_derivatives.stem: [
            x.parent.stem for x in list(s.session_path_raw.rglob("*.ap.bin"))
        ]

        for s in mtd.sessions
    }
    if len(sessions_and_runs.values()) == 0:
        print("no runs found")
        raise ValueError()

    t = time.time()
    print("using new edits")
    run_full_pipeline(
        base_path=base_path,
        sub_name=mtd.mouse_id,
        sessions_and_runs=sessions_and_runs,
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
