from __future__ import annotations

import contextlib
import datetime
import itertools
import json
import logging
from typing import ClassVar, Literal

import codeocean.computation
import codeocean.data_asset
import npc_session
import upath

import aind_session.extension
import aind_session.utils.codeocean_utils

logger = logging.getLogger(__name__)


@aind_session.extension.register_namespace("ecephys")
class EcephysExtension(aind_session.extension.ExtensionBaseClass):
    """Extension providing an ecephys modality namespace, for handling sorted data
    assets etc.

    Examples
    --------
    >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
    >>> session.ecephys.latest_ks25_sorted_data_asset.id
    'a2a54575-b5ca-4cf0-acd0-2933e18bcb2d'
    >>> session.ecephys.latest_ks25_sorted_data_asset.name
    'ecephys_676909_2023-12-13_13-43-40_sorted_2024-03-01_16-02-45'
    >>> session.ecephys.clipped_dir.as_posix()
    's3://aind-ephys-data/ecephys_676909_2023-12-13_13-43-40/ecephys_clipped'
    """

    SORTING_PIPELINE_ID: ClassVar[str] = "1f8f159a-7670-47a9-baf1-078905fc9c2e"
    TRIGGER_CAPSULE_ID: ClassVar[str] = "eb5a26e4-a391-4d79-9da5-1ab65b71253f"

    @property
    def sorted_data_assets(self) -> tuple[codeocean.data_asset.DataAsset, ...]:
        """All sorted data assets associated with the session (may be empty).

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.sorted_data_assets[0].id
        '1e11bdf5-b452-4fd9-bbb1-48383a9b0842'
        >>> session.ecephys.sorted_data_assets[0].name
        'ecephys_676909_2023-12-13_13-43-40_sorted_2023-12-17_03-16-51'
        >>> session.ecephys.sorted_data_assets[0].created
        1702783011

        Empty if no sorted data assets are found:
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-39')
        >>> session.ecephys.sorted_data_assets
        ()
        """
        assets = tuple(
            asset
            for asset in self._session.data_assets
            if self.is_sorted_data_asset(asset)
        )
        logger.debug(
            f"Found {len(assets)} sorted data asset{'' if len(assets) == 1 else 's'} for {self._session.id}"
        )
        return assets

    @staticmethod
    def is_sorted_data_asset(asset_id: str | codeocean.data_asset.DataAsset) -> bool:
        """Check if the asset is a sorted data asset.

        - assumes sorted asset to be named <session-id>_sorted<unknown-suffix>
        - does not assume platform to be `ecephys`

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.is_sorted_data_asset('173e2fdc-0ca3-4a4e-9886-b74207a91a9a')
        True
        >>> session.ecephys.is_sorted_data_asset('83636983-f80d-42d6-a075-09b60c6abd5e')
        False
        """
        asset = aind_session.utils.codeocean_utils.get_data_asset_model(asset_id)
        try:
            session_id = str(npc_session.AINDSessionRecord(asset.name))
        except ValueError:
            logger.debug(
                f"{asset.name=} does not contain a valid session ID: determined to be not a sorted data asset"
            )
            return False
        if asset.name.startswith(f"{session_id}_sorted"):
            logger.debug(
                f"{asset.name=} determined to be a sorted data asset based on name starting with '<session-id>_sorted'"
            )
            return True
        else:
            logger.debug(
                f"{asset.name=} determined to be not a sorted data asset based on name starting with '<session-id>_sorted'"
            )
            return False

    @property
    def is_sorted(self) -> bool:
        """Check if a sorted data asset exists, and is not in an error state.

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.is_sorted
        True
        """
        if not self.sorted_data_assets:
            return False
        if self.is_sorting_fail:
            return False
        return True

    @property
    def latest_ks25_sorted_data_asset(self) -> codeocean.data_asset.DataAsset:
        """Latest sorted data asset associated with the session.

        Raises `AttributeError` if no sorted data assets are found.

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> asset = session.ecephys.latest_ks25_sorted_data_asset
        >>> asset.id        # doctest: +SKIP
        'a2a54575-b5ca-4cf0-acd0-2933e18bcb2d'
        >>> asset.name      # doctest: +SKIP
        'ecephys_676909_2023-12-13_13-43-40_sorted_2024-03-01_16-02-45'
        >>> asset.created   # doctest: +SKIP
        1709420992
        """
        return self.get_latest_sorted_data_asset(sorter_name="kilosort2_5")

    def get_latest_sorted_data_asset(
        self,
        sorter_name: str | None = "kilosort2_5",
    ) -> codeocean.data_asset.DataAsset:
        """Get the latest sorted data asset associated with the session.

        - if `sorter_name` is None, the latest sorted data asset is returned
          regardless of the sorter used
        - raises `AttributeError` if no sorted data assets are found
        - raises `ValueError` if the sorter name does not match the expected value

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> asset = session.ecephys.get_latest_sorted_data_asset()
        >>> asset.id        # doctest: +SKIP
        'a2a54575-b5ca-4cf0-acd0-2933e18bcb2d'
        >>> asset.name      # doctest: +SKIP
        'ecephys_676909_2023-12-13_13-43-40_sorted_2024-03-01_16-02-45'
        >>> asset.created   # doctest: +SKIP
        1709420992
        """
        if len(self.sorted_data_assets) == 1:
            asset = self.sorted_data_assets[0]
        elif len(self.sorted_data_assets) > 1:
            asset = aind_session.utils.sort_by_created(self.sorted_data_assets)[-1]
            created = datetime.datetime.fromtimestamp(asset.created).isoformat(sep=" ")
            logger.info(
                f"Found {len(self.sorted_data_assets)} sorted data assets for {self._session.id}: most recent asset will be used ({created=})"
            )
        else:
            raise AttributeError(
                f"No sorted data assets found for {self._session.id}:",
                (
                    " raw data has not been uploaded yet."
                    if not self._session.is_uploaded
                    else " try session.ecephys.run_sorting()"
                ),
            )
        if sorter_name is not None:
            if (sorter := self.get_sorter_name(asset)) != sorter_name:
                raise ValueError(
                    f"Expected sorter name {sorter_name!r} but found {sorter!r} for {asset.id=}"
                )
        logger.debug(f"Using {asset.id=} for {self._session.id} sorted data asset")
        return asset

    @property
    def sorted_data_dir(self) -> upath.UPath:
        """Path to the dir containing the latest sorted data associated with the
        session, likely in an S3 bucket.

        - uses latest sorted data asset to get path (existence is checked)
        - if no sorted data asset is found, checks for a data dir in S3
        - raises `AttributeError` if no sorted data assets are available to link
          to the session

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.sorted_data_dir.as_posix()
        's3://codeocean-s3datasetsbucket-1u41qdg42ur9/a2a54575-b5ca-4cf0-acd0-2933e18bcb2d'
        """
        try:
            _ = self.latest_ks25_sorted_data_asset
        except AttributeError:
            raise AttributeError(
                f"No sorted data asset found in CodeOcean for {self._session.id}. Has the session been sorted?"
            ) from None
        else:
            logger.debug(
                f"Using asset {self.latest_ks25_sorted_data_asset.id} to find sorted data path for {self._session.id}"
            )
            sorted_data_dir = (
                aind_session.utils.codeocean_utils.get_data_asset_source_dir(
                    asset_id=self.latest_ks25_sorted_data_asset.id
                )
            )
            logger.debug(
                f"Sorted data path found for {self._session.id}: {sorted_data_dir}"
            )
            return sorted_data_dir

    @property
    def clipped_dir(self) -> upath.UPath:
        """Path to the dir containing original Open Ephys recording data, with
        truncated `continuous.dat` files.

        - originally located in the root of the session's raw data dir
        - for later sessions (2024 onwards), located in an `ecephys` subdirectory

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.clipped_dir.as_posix()
        's3://aind-ephys-data/ecephys_676909_2023-12-13_13-43-40/ecephys_clipped'
        """
        if (
            path := self.get_clipped_and_compressed_dirs(
                self._session.raw_data_asset.id
            )[0]
        ) is None:
            raise AttributeError(
                f"No 'clipped' dir found in uploaded raw data for {self._session.id} (checked in root dir and modality subdirectory)"
            )
        return path

    @property
    def compressed_dir(self) -> upath.UPath:
        """
        Path to the dir containing compressed zarr format versions of Open Ephys
        recording data (AP and LFP).

        - originally located in the root of the session's raw data dir
        - for later sessions (2024 onwards), located in an `ecephys` subdirectory

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.compressed_dir.as_posix()
        's3://aind-ephys-data/ecephys_676909_2023-12-13_13-43-40/ecephys_compressed'
        """
        if (
            path := self.get_clipped_and_compressed_dirs(
                self._session.raw_data_asset.id
            )[1]
        ) is None:
            raise AttributeError(
                f"No 'compressed' dir found in uploaded raw data for {self._session.id} (checked in root dir and modality subdirectory)"
            )
        return path

    @staticmethod
    def get_clipped_and_compressed_dirs(
        raw_data_asset_id_or_model: str | codeocean.data_asset.DataAsset,
    ) -> tuple[upath.UPath | None, upath.UPath | None]:
        """
        Paths to the dirs containing Open Ephys recording data in CodeOcean upload
        dir.

        - originally located in the root of the session's raw data dir
        - for later sessions (2024 onwards), located in an `ecephys` subdirectory

        Examples
        --------
        >>> clipped, compressed = aind_session.ecephys.get_clipped_and_compressed_dirs('16d46411-540a-4122-b47f-8cb2a15d593a')
        >>> clipped.as_posix()
        's3://aind-ephys-data/ecephys_676909_2023-12-13_13-43-40/ecephys_clipped'
        """
        asset_id = aind_session.utils.codeocean_utils.get_normalized_uuid(
            raw_data_asset_id_or_model
        )
        raw_data_dir = aind_session.utils.get_data_asset_source_dir(asset_id=asset_id)
        candidate_parent_dirs = (
            raw_data_dir / "ecephys",  # newer location in dedicated modality folder
            raw_data_dir,  # original location in root if upload folder
        )
        return_paths: list[upath.UPath | None] = [None, None]
        for parent_dir in candidate_parent_dirs:
            for i, name in enumerate(("clipped", "compressed")):
                if (path := parent_dir / f"ecephys_{name}").exists():
                    if (existing_path := return_paths[i]) is None:
                        return_paths[i] = path
                        logger.debug(f"Found {path.as_posix()}")
                    else:
                        assert existing_path is not None
                        logger.info(
                            f"Found multiple {name} dirs: using {existing_path.relative_to(raw_data_dir).as_posix()} over {path.relative_to(raw_data_dir).as_posix()}"
                        )
        assert len(return_paths) == 2
        return return_paths[0], return_paths[1]

    @property
    def sorted_probes(self) -> tuple[str, ...]:
        """Names of probes that reached the final stage of the sorting pipeline.

        - checks for probe dirs in the session's latest sorted data dir
        - checks a specific dir that indicates all processing completed:
            - `sorting_precurated` was original dir name, then changed to `curated`
        - probe folders named `experiment1_Record Node
          104#Neuropix-PXI-100.ProbeF-AP_recording1` - from which `ProbeF` would
          be extracted
        - does not represent the recordings that were sorted

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.sorted_probes
        ('ProbeA', 'ProbeB', 'ProbeC', 'ProbeD', 'ProbeE', 'ProbeF')
        >>> session = aind_session.Session('ecephys_728537_2024-08-21_17-41-36')
        >>> session.ecephys.sorted_probes
        ('46100', '46110')
        """
        return self.get_sorted_probe_names(self.latest_ks25_sorted_data_asset.id)

    @staticmethod
    def get_sorted_probe_names(
        sorted_data_asset_id_or_model: str | codeocean.data_asset.DataAsset,
    ) -> tuple[str, ...]:
        """Names of probes that reached the final stage of the sorting pipeline.

        - checks for probe dirs in the asset's data dir
        - checks a specific dir that indicates all processing completed:
            - `sorting_precurated` was original dir name, then changed to `curated`
        - probe folders named `experiment1_Record Node
          104#Neuropix-PXI-100.ProbeF-AP_recording1` - from which `ProbeF` would
          be extracted

        Examples
        --------
        >>> aind_session.ecephys.get_sorted_probe_names('a2a54575-b5ca-4cf0-acd0-2933e18bcb2d')
        ('ProbeA', 'ProbeB', 'ProbeC', 'ProbeD', 'ProbeE', 'ProbeF')
        """
        asset_id = aind_session.utils.codeocean_utils.get_normalized_uuid(
            sorted_data_asset_id_or_model
        )
        sorted_data_dir = aind_session.utils.get_data_asset_source_dir(
            asset_id=asset_id
        )
        candidate_parent_dirs = (
            sorted_data_dir / "curated",
            sorted_data_dir / "sorting_precurated",
        )
        for parent_dir in candidate_parent_dirs:
            if parent_dir.exists():
                break
        else:
            logger.info(
                f"No 'curated' or 'sorting_precurated' dir found in {sorted_data_dir.as_posix()}: assuming no probes completed processing"
            )
            return ()
        probes = set()
        for path in parent_dir.iterdir():
            # e.g. experiment1_Record Node 104#Neuropix-PXI-100.ProbeF-AP_recording1
            probe = (
                path.name.split(".")[1]
                .split("_recording")[0]
                .removesuffix("-AP")
                .removesuffix("-LFP")
            )
            probes.add(probe)
        logger.debug(f"Found {len(probes)} probes in {parent_dir.as_posix()}: {probes}")
        return tuple(sorted(probes))

    @property
    def is_sorting_fail(self) -> bool:
        """Check if the latest sorted data asset indicates that the sorting pipeline failed.

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> session.ecephys.is_sorting_fail
        False
        """
        return aind_session.utils.codeocean_utils.is_data_asset_error(
            self.latest_ks25_sorted_data_asset
        )

    def run_sorting(
        self,
        pipeline_type: Literal[
            "ecephys", "ecephys_opto", "ecephys_analyzer"
        ] = "ecephys",
        trigger_capsule_id: str = "eb5a26e4-a391-4d79-9da5-1ab65b71253f",
        override_parameters: list[str] | None = None,
        skip_already_sorting: bool = True,
    ) -> codeocean.computation.Computation | None:
        """Run the sorting trigger capsule with the session's raw data asset
        (assumed to be only one). Launches the sorting pipeline then creates a new
        sorted data asset.

        - **note: the trigger capsule needs user secrets attached in order to run**
        - defaults to this capsule:
            https://codeocean.allenneuraldynamics.org/capsule/6726080/tree
        - the capsule uses positional arguments, so passing extra parameters is
          currently awkward: will update to pass named parameter kwargs in the
          future
            - if needed, you can override the parameters used with a custom list
        - if `skip_already_sorting` is `True`, a new pipeline run will not
          triggered the session's raw data asset is already being sorted (returns
          None)

        Examples
        --------
        >>> session = aind_session.Session('ecephys_676909_2023-12-13_13-43-40')
        >>> computation = session.ecephys.run_sorting()       # doctest: +SKIP

        # Supply list of positional arguments (pipeline type and data asset ID are
        required)
        >>> override_parameters = ['ecephys_opto', session.raw_data_asset.id]
        >>> session.ecephys.run_sorting(override_parameters) # doctest: +SKIP
        """
        if override_parameters:
            if len(override_parameters) < 2:
                raise ValueError(
                    "At least two parameters are required: data asset ID is the second parameter. See https://codeocean.allenneuraldynamics.org/capsule/6726080/tree"
                )
            logger.debug("Using custom parameters to trigger sorting pipeline")
            parameters = override_parameters
            asset = aind_session.utils.codeocean_utils.get_data_asset_model(
                parameters[1]
            )
        else:
            asset = self._session.raw_data_asset
            parameters = [pipeline_type, asset.id]
        if skip_already_sorting:
            current_computations = (
                aind_session.utils.codeocean_utils.search_computations(
                    capsule_or_pipeline_id=self.SORTING_PIPELINE_ID,
                    attached_data_asset_id=asset.id,
                    in_progress=True,
                    ttl_hash=aind_session.utils.get_ttl_hash(
                        1
                    ),  # 1 sec, we want a current check
                )
            )
            if current_computations:
                logger.warning(
                    f"Sorting is already running for {asset.id}: {[c.name for c in current_computations]}. Use `skip_already_sorting=False` to force a new pipeline run"
                )
                return None
        logger.debug(f"Triggering sorting pipeline with {parameters=}")
        computation = aind_session.utils.codeocean_utils.get_codeocean_client().computations.run_capsule(
            codeocean.computation.RunParams(
                capsule_id=trigger_capsule_id,
                parameters=parameters,
            )
        )
        logger.info(
            f"Triggered sorting pipeline for {asset.id} {asset.name}: monitor {computation.name!r} at https://codeocean.allenneuraldynamics.org/capsule/6726080/tree"
        )
        return computation

    @property
    def current_sorting_computations(
        self,
    ) -> tuple[codeocean.computation.Computation, ...]:
        """
        All sorting pipeline computations that have the session's raw data asset
        attached and have not finished.

        - running defined as `computation.end_status is None`
        - sorted by ascending creation time
        - defaults to https://codeocean.allenneuraldynamics.org/capsule/8510735/tree
            - can be overridden with a different pipeline ID
        Examples
        --------
        >>> session = aind_session.Session('ecephys_733887_2024-08-16_12-16-49')
        >>> computations = session.ecephys.current_sorting_computations
        >>> [c.name for c in computations]   # doctest: +SKIP
        ['Run With Parameters 4689084']
        """
        return aind_session.utils.codeocean_utils.search_computations(
            capsule_or_pipeline_id=self.SORTING_PIPELINE_ID,
            attached_data_asset_id=self._session.raw_data_asset.id,
            in_progress=True,
            ttl_hash=aind_session.utils.get_ttl_hash(1 * 60),
        )

    @staticmethod
    def get_sorter_name(data_asset_id: str | codeocean.data_asset.DataAsset) -> str:
        """
        Get the version of the Kilosort pipeline used to create the sorted data asset.

        Tries to find `sorter_name` in the following json files, in order, for any
        probe:
        - `processing.json` (in root of asset)
        - `si_folder.json` (in `spikesorted` dir)
        - `sorting.json` (in `postprocessed` dir)
        - `params.json` (in root of asset, for older assets)

        Raises `ValueError` if none of the json files exist, or if none contain the
        `sorter_name` key, either of which indicates that the asset data is
        incomplete due to the sorting pipeline failing for all probes.

        Examples
        --------

        - processing.json['processing_pipeline']['data_processes'][index]['parameters']['sorter_name']:
        >>> aind_session.ecephys.get_sorter_name('921a186a-d8ff-4efc-8e1a-891fde8cd394')
        'kilosort2_5'

        - processing.json['processing_pipeline']['data_processes'][index]['parameters']['sorter_name']:
        >>> aind_session.ecephys.get_sorter_name('01d9d159-96f0-43f1-9d14-29b5c2521d94')
        'kilosort4'

        - processing.json['data_processes'][index]['parameters']['sorter_name']:
        >>> aind_session.ecephys.get_sorter_name('205fc2d0-5f00-468f-a82d-47c94afcd40c')
        'kilosort2_5'

        - spikesorted/si_folder.json['annotations']['__sorting_info__']['params']['sorter_name']:
        >>> aind_session.ecephys.get_sorter_name('bd0ad804-4a33-4613-9d6c-6281e442bade')
        'kilosort2_5'

        - params.json['spikesorting']['sorter_name']
        >>> aind_session.ecephys.get_sorter_name('0eca2d35-5c8c-48bb-a921-e48cf3d871de')
        'kilosort2_5'

        - no sorter_name available:
        >>> aind_session.ecephys.get_sorter_name('b4a7757c-6826-49eb-b3dd-d6cd871c5e7c')
        Traceback (most recent call last):
        ...
        ValueError: Sorting data are incomplete for
        data_asset_id='b4a7757c-6826-49eb-b3dd-d6cd871c5e7c' (pipeline likely failed) - cannot get sorter name
        """
        source_dir = aind_session.utils.codeocean_utils.get_data_asset_source_dir(
            aind_session.utils.codeocean_utils.get_normalized_uuid(data_asset_id)
        )

        def _get_sorter_name_from_processing_json(source_dir: upath.UPath) -> str:
            processing_path = source_dir / "processing.json"
            if not processing_path.exists():
                raise FileNotFoundError(f"No 'processing.json' found in {source_dir}")
            processing_text = processing_path.read_text()
            if '"sorter_name":' not in processing_text:
                raise KeyError(
                    f"No 'sorter_name' value found in processing.json for {data_asset_id=}"
                )
            processing: dict = json.loads(processing_text)
            if "processing_pipeline" in processing:
                data_processes = processing["processing_pipeline"]["data_processes"]
            else:
                assert (
                    "data_processes" in processing
                ), f"Fix method of getting sorter name: 'data_processes' not in processing.json for {data_asset_id=}"
                data_processes = processing["data_processes"]
            for p in data_processes:
                if isinstance(p, list):
                    sorting: dict = next(
                        (d for d in p if d.get("name") == "Spike sorting"),
                        {},
                    )
                    break
                else:
                    if p.get("name") == "Spike sorting":
                        sorting = p
                        break
            else:
                raise AssertionError(
                    f"Fix method of getting sorter name: 'sorter_name' is in processing.json, but not in expected location for {data_asset_id=}"
                )
            assert (
                "parameters" in sorting
            ), f"Fix method of getting sorter name: 'parameters' not in 'Spike sorting' data process in processing.json for {data_asset_id=}"
            if "sorter_name" not in sorting["parameters"]:
                raise KeyError(
                    "No 'sorter_name' key found in sorting parameters in processing.json"
                )
            sorter_name: str = sorting["parameters"]["sorter_name"]
            logger.debug(f"Found sorter_name key in processing.json: {sorter_name}")
            return sorter_name

        def _get_sorter_name_from_sorted_folders(source_dir: upath.UPath) -> str:
            json_paths = []
            for json_path in itertools.chain(
                (source_dir / "spikesorted").rglob("si_folder.json"),
                (source_dir / "postprocessed").rglob("sorting.json"),
            ):
                json_paths.append(json_path)
                info = json_path.read_text()
                if '"sorter_name":' in info:
                    sorter_name = json.loads(info)["annotations"]["__sorting_info__"][
                        "params"
                    ]["sorter_name"]
                    logger.debug(
                        f"Found sorter_name key in {json_path.name}: {sorter_name}"
                    )
                    return sorter_name
            else:
                if not json_paths:
                    raise FileNotFoundError(
                        f"No 'processing.json', 'si_folder.json', or 'sorting.json' files found - asset {data_asset_id} likely contains incomplete data"
                    )
                else:
                    raise KeyError(
                        f"Fix method of getting sorter name: 'sorter_name' not a value in {set(p.name for p in json_paths)} for {data_asset_id=}"
                    )

        def _get_sorter_name_from_params_json(source_dir: upath.UPath) -> str:
            params_path = source_dir / "params.json"
            if not params_path.exists():
                raise FileNotFoundError(f"No 'params.json' found in {source_dir}")
            params_text = params_path.read_text()
            if '"sorter_name":' not in params_text:
                raise KeyError(f"No 'sorter_name' key found in {params_path.name}")
            params: dict = json.loads(params_text)
            assert (
                params
            ), f"Fix method of getting sorter name: {params=} for {data_asset_id=}"
            assert (
                "spikesorting" in params
            ), f"Fix method of getting sorter name: 'spikesorting' not in {params_path.name} for {data_asset_id=}"
            assert (
                "sorter_name" in params["spikesorting"]
            ), f"Fix method of getting sorter name: 'sorter_name' not in 'spikesorting' in {params_path.name} for {data_asset_id=}"
            sorter_name = params["spikesorting"]["sorter_name"]
            logger.debug(f"Found sorter_name key in params.json: {sorter_name}")
            return sorter_name

        with contextlib.suppress(FileNotFoundError, KeyError):
            return _get_sorter_name_from_processing_json(source_dir)
        with contextlib.suppress(FileNotFoundError, KeyError):
            return _get_sorter_name_from_sorted_folders(source_dir)
        with contextlib.suppress(FileNotFoundError, KeyError):
            return _get_sorter_name_from_params_json(source_dir)
        raise ValueError(
            f"Sorting data are incomplete for {data_asset_id=!r} (pipeline likely failed) - cannot get sorter name"
        )


if __name__ == "__main__":
    from aind_session import testmod

    testmod()
