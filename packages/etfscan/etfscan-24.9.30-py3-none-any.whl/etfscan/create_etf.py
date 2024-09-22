import argparse
import os
import h5py
from scipy import ndimage
import numpy as np
from nxtomomill.app import h52nx as nxmill_app
import shutil
from namedlist import namedlist
from .etf import ETFFile


def get_arguments():


    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--bliss_file",
        required=False,
        help=f"""a bliss master file. One and only one of --bliss_file, --nexus_file, --etf_projections_dir must be provided """,
        type = str
    )
    parser.add_argument(
        "--nexus_file",
        required=False,
        help=f"""a nexus file produce by nx tomomill """,
        type = str
    )

    parser.add_argument(
        "--etf_projections_dir",
        required=False,
        help=f"""The projections will be taken from the projections.h5 file inside etf_projections_dir. Must be available inside a etf directory """,
        type = str
    )
    
    parser.add_argument(
        "--darks_flats_dir",
        required=False,
        help=f"""a nexus file produce by nx tomomill. Will be searched to associate the dark/flats to the nexus_file, if nexus_file is provided """,
        type = str
    )

    parser.add_argument(
        "--etf_dark_dir",
        required=False,
        help=f"""The dark will be taken from the dark.h5 file inside etf_dark_dir. Must be available inside a etf directory """,
        type = str
    )
    parser.add_argument(
        "--etf_flats_dir",
        required=False,
        help=f"""The flats will be taken from the flats.h5 file inside etf_flats_dir. Must be available inside a etf directory """,
        type = str
    )

    
    parser.add_argument(
        "--entry_name",
        required=False,
        default="entry0000",
        help=f"""the entry name """,
        type = str
    )

    parser.add_argument(
        "--target_dir",
        required=False,
        help=f"""The path where the etf will be written. Defaults to the current work directory""",
        type = str
    )
    parser.add_argument(
        "--target_name",
        required=False,
        help=f"""How the etf will be named. Defaults to the nx/bliss filename if they are given. If --etf_projections_dir is used, the it becomes mandatory""",
        type = str
    )
    parser.add_argument(
        "--median_dark",
        action="store_true",
        help=f"""Median will be used instead of average in darks. It is not used if. Used if dark come from nexus  """,
    )
    parser.add_argument(
        "--median_flat",
        action="store_true",
        help=f"""Median will be used instead of average in flats. Used if flats come from nexus """,
    )
    
    parser.add_argument(
        "--double_flats_file",
        required=False,
        help=f"""The double_flats file""",
        type = str
    )
    
    parser.add_argument(
        "--diffusion_correction_file",
        required=False,
        help=f"""The diffusion correction file""",
        type = str
    )
    
    parser.add_argument(
        "--distortion_correction_file",
        required=False,
        help=f"""The detector real positions map""",
        type = str
    )
    parser.add_argument(
        "--weight_map_file",
        required=False,
        help=f"""The weight map""",
        type = str
    )
    
    args = parser.parse_args()

    args = arguments_postprocessing(args)

    return args
    
def  arguments_postprocessing(args):
    if hasattr(args, "_fields"):

        
        possibly_missing_items =  dict( tuple([( field, None  ) for field in
                                            ["target_scan_dir", "nx_data_path", "flats_file",
                                             "darks_file",
                                             "control_keys", "entry"
                                             "globals_indexes","median_flat","median_dark",
                                             "etf_projections_dir", "etf_dark_dir", "etf_flats_dir",
                                             "target_name"
                                            ]])
        )

        given_args = dict(tuple(args._asdict().items()))

        possibly_missing_items.update(  given_args )

        all_pars = possibly_missing_items
        
        args = namedlist("EditedArgs",   tuple(all_pars.items()) ) ()


        
    possible_projection_sources = (args.bliss_file, args.nexus_file,  etf_projections_dir)
    non_none_count = sum(1 for item in (args.bliss_file, args.nexus_file,  etf_projections_dir) if item is not None)
    if non_none_count != 1:
        message = "One and only one source for the projections must be provided"
        raise ValueError(message)

        
    args.target_dir = args.target_dir or os.path.realpath(os.curdir)
    
    if args.bliss_file is not None:
        if args.target_name is None:
            args.target_name = args.target_name or os.path.splitext(os.path.basename(args.bliss_file))[0] + ".etf"
        # in this case the nexus file will be an intermediate and will be place in the etf directory

        place_nexus_file_in_target_scan_dir = True
        
        if args.nexus_file is None:
            args.nexus_file =  os.path.splitext(os.path.basename(args.bliss_file))[0] + ".nx"
        else:
            args.nexus_file = os.path.basename(  args.nexus_file ) 

    elif args.bliss_file is not None:
        args.nexus_file = os.path.realpath(args.nexus_file)
        place_nexus_file_in_target_scan_dir = True
        if args.target_name is None:
            with h5py.File(  args.nexus_file  ,"r") as fr:
                _tmp_names = fr[f"/{args.entry_name}/bliss_original_files"][()]
                if len ( _tmp_names ):
                    original_file_name = _tmp_names[0].decode('utf-8')
                else:
                    original_file_name = args.nexus_file
                
                original_file_name  = os.path.splitext(os.path.basename(original_file_name))[0]
                args.target_name =  original_file_name  + ".etf"
    else:
        place_nexus_file_in_target_scan_dir = False
        if args.target_name is None:
            with h5py.File(  os.path.join(args.etf_projections_dir,"projections.h5")  ,"r") as fr:
                _tmp_names = fr[f"/globals/bliss_original_files"][()]
                if len ( _tmp_names ):
                    original_file_name = _tmp_names[0].decode('utf-8')
                else:
                    original_file_name = args.nexus_file
                    

    if not len(os.path.splitext(args.target_name)[1]):
        args.target_name = args.target_name + ".etf"

    args.target_scan_dir = os.path.join( args.target_dir, args.target_name)
    os.makedirs(args.target_scan_dir, exist_ok=True)
    
    if place_nexus_file_in_target_scan_dir:
        args.nexus_file = os.path.join( args.target_scan_dir,  args.nexus_file )

    args.nx_data_path = f"/{args.entry_name}/instrument/detector/data"
    

    if args.darks_flats_dir is None:
        args.darks_flats_dir = os.path.dirname(os.path.realpath(args.nexus_file))

    

    print(" QUI ", args.darks_flats_dir, args.nexus_file ) 
    args.flats_file = os.path.join(args.darks_flats_dir, os.path.splitext(os.path.basename(args.nexus_file))[0] +"_flats.hdf5")
    args.darks_file = os.path.join(args.darks_flats_dir, os.path.splitext(os.path.basename(args.nexus_file))[0] +"_darks.hdf5")


    if not( os.path.isfile(args.flats_file) ):
        args.flats_file = None
    if not( os.path.isfile(args.darks_file) ):
        args.darks_file = None

    return args


def main(args=None):
    
    if args is None:
        args = get_arguments()
    else:
        args = arguments_postprocessing(args)

    if args.etf_projections_dir is not None:
        create_etf_from_etf(args)
    else:
        create_etf_from_bliss_nexus(args)


    do_flats_and_darks(args)
        
def create_etf_from_bliss_nexus(args):
    if args.bliss_file is not None:
        os.environ["TOMOTOOLS_SKIP_DET_CHECK"] = "1"
        nxmill_app.main(  [ "h52nx" ,  args.bliss_file, args.nexus_file,  "--overwrite"] ) 
        print("Done with nxtomomill")

        
    with h5py.File( args.nexus_file ,"r") as f:
    
        # not elegant hard coded entry0000 and paths. 
        n_tot_images, dim_z, dim_x = f[args.nx_data_path].shape

        print( " READING ", args.nexus_file  )
        data_dtype = f[f"/{args.entry_name}/instrument/detector/data"].dtype
        print(" OK ")
        args.control_keys = f[f"/{args.entry_name}/instrument/detector/image_key"][()]

    n_projections = np.equal(0, args.control_keys).sum()

    new_layout = h5py.VirtualLayout(shape= (n_projections, dim_z, dim_x) , dtype= data_dtype)

    args.globals_indexes = np.arange(len(args.control_keys))

    # PROJECTIONS
    
    labeled_regions, nregions = ndimage.label(  np.equal( 0, args.control_keys  ) )
    
    unwrapped_angles = None
    
    if nregions:
        stack_height = 0
    
        for label in range( 1 , nregions+1):
            region_start = args.globals_indexes[  labeled_regions == label    ].min()
            region_end   = 1 + args.globals_indexes[  labeled_regions == label    ].max()
    
            vsource = h5py.VirtualSource(args.nexus_file, args.nx_data_path, [n_tot_images,  dim_z, dim_x]  )
            new_layout[ stack_height : stack_height + ( region_end - region_start ) ] = vsource[region_start:region_end]
    
            stack_height +=  region_end - region_start
    
        with h5py.File( os.path.join(args.target_scan_dir,"projections.h5"), "w" ) as fw, h5py.File( args.nexus_file ,"r") as fr :
            fw.create_virtual_dataset("data", new_layout, fillvalue=0)
    
            fw.create_group("globals")
            fw["globals/beam_energy_kev"] = fr[f"/{args.entry_name}/beam/incident_energy"][()]
            fw["globals/bliss_original_files"] = fr[f"/{args.entry_name}/bliss_original_files"][()]
            fw["globals/distance_m"] = fr[f"/{args.entry_name}/instrument/detector/distance"][()]
            fw["globals/estimated_cor_from_motor_pixel"] =  fr[f"/{args.entry_name}/instrument/detector/estimated_cor_from_motor"][()]
            
            fw["globals/x_pixel_size_m"] =fr[f"/{args.entry_name}/instrument/detector/x_pixel_size"][()]
            fw["globals/y_pixel_size_m"] =fr[f"/{args.entry_name}/instrument/detector/y_pixel_size"][()]
            
            fw.create_group("framewise")
            fw["framewise/control"] = fr[f"/{args.entry_name}/control/data"][ labeled_regions > 0  ]
            angles = fr[f"/{args.entry_name}/data/rotation_angle"][  labeled_regions > 0 ]

            # but angles are not discarded, they have more digits than the unwrapped ones
            unwrapped_angles = np.unwrap(angles, period=360)
            # the correspondence index->angle will be used to tag the flats with unwrapped angles
            unwrapped_angles_indexes = args.globals_indexes[  labeled_regions > 0    ]
            
            fw["framewise/angles_deg"] = angles
            fw["framewise/unwrapped_angles_deg"] = unwrapped_angles
            if f"/{args.entry_name}/instrument/detector/count_time" in fr :
                fw["framewise/count_time"] = fr[f"/{args.entry_name}/instrument/detector/count_time"][labeled_regions > 0]
                
            if f"/{args.entry_name}/instrument/detector/estimated_cor_from_motors" in fr :
                fw["globals/count_estimated_cor_from_motors"] = fr[f"/{args.entry_name}/instrument/detector/estimated_cor_from_motors"]
                
            fw["framewise/x_translation_m"] = fr[f"/{args.entry_name}/sample/x_translation"][labeled_regions > 0]
            fw["framewise/y_translation_m"] = fr[f"/{args.entry_name}/sample/y_translation"][labeled_regions > 0]
            fw["framewise/z_translation_m"] = fr[f"/{args.entry_name}/sample/z_translation"][labeled_regions > 0]
        


def create_etf_from_etf(args):

    
    etffile = ETFFile( os.path.join(args.etf_projections_dir,"projections.h5")  )

    etffile.save(  args.target_name, target_dir = args.target_dir,    ftype="projections"  )
    
def copy_etf_dark(args):
    
    etffile = ETFFile( os.path.join(args.etf_dark_dir,"dark.h5")  )

    etffile.save(  args.target_name, target_dir = args.target_dir,   ftype="dark"  )

    with h5py.File( os.path.join(args.target_scan_dir,"dark.h5"), "r" ) as fr:
        dark = fr["data"][()]
    return dark

    

def copy_etf_flats(args):
    
    etffile = ETFFile( os.path.join(args.etf_dark_dir,"flats.h5")  )

    etffile.save(  args.target_name, target_dir = args.target_dir,   ftype="flats"  )

    


def do_flats_and_darks(args):


    if args.etf_dark_dir:
        dark = copy_etf_dark(args)
    else:
        if args.darks_file is None:
            dark = extract_darks_file_from_nx(args)
        else:
            dark = adapt_darks(args)


            
    # FLATS

    if args.etf_flats_dir:
        copy_etf_flats(args)
    else:
        if args.flats_file is None:
            extract_flats_from_nx(args, dark,  unwrapped_angles_indexes , unwrapped_angles )
        else:
            adapt_flats(args, unwrapped_angles_indexes , unwrapped_angles )


    # data for other preprocessings 
        
    if args.double_flats_file is not None:
        adapt_double_flats(args )

    if args.diffusion_correction_file is not None:
        adapt_diffusion(args )
        
    if args.distortion_correction_file is not None:
        adapt_distortion_correction(args )
        
    if args.weight_map_file is not None:
        adapt_weight_map(args )




        
def adapt_double_flats(args ):
    shutil.copyfile(args.double_flats_file , os.path.join(args.target_scan_dir,"double_flats.h5"))
    
def adapt_diffusion(args ):
    shutil.copyfile(args.diffusion_correction_file , os.path.join(args.target_scan_dir,"diffusion_correction.h5"))

def adapt_distortion_correction(args ):
    shutil.copyfile(args.distortion_correction_file , os.path.join(args.target_scan_dir,"distortion_correction.h5"))

def adapt_flats(args,   unwrapped_angles_indexes , unwrapped_angles  ):

    with  h5py.File( args.flats_file ,"r") as fr :
        path = f"/{args.entry_name}/flats"
        group = fr[path]

        image_keys = [key for key in group.keys() if key.isnumeric()]
        image_keys.sort(key=int)
        first_image = group[image_keys[0]][()]
        image_shape = first_image.shape
        stack = np.zeros((len(image_keys), *image_shape), dtype=first_image.dtype)
        for i, key in enumerate(image_keys):
            stack[i] = group[key][()]

        key_values = list(map(int,image_keys))

        assert (len(unwrapped_angles_indexes) == len(unwrapped_angles) ),"must have the same length"
        
        flat_angles_unwrapped = np.interp( key_values,  unwrapped_angles_indexes , unwrapped_angles   )

        flat_currents = group["machine_electric_current"][()]
        
    with h5py.File( os.path.join(args.target_scan_dir,"flats.h5"), "w" ) as fw:
        fw["data"] = stack
        fw.create_group("framewise")
        fw["framewise/flats_currents"] = flat_currents
        fw["framewise/flats_angles_unwrapped"] = flat_angles_unwrapped
        


def adapt_weight_map(args ):

    with  h5py.File( args.weight_map_file ,"r") as fr :
        path = f"/{args.entry_name}/weights_field/results/data"
        data = fr[path][()]
        
    with h5py.File( os.path.join(args.target_scan_dir,"weight_map.h5"), "w" ) as fw:
        fw["data"] = data
        
def adapt_darks(args):        

    with  h5py.File( args.darks_file ,"r") as fr :
        dark = fr[f"/{args.entry_name}/darks/0"][()] 

    with h5py.File( os.path.join(args.target_scan_dir,"dark.h5"), "w" ) as fw:
        fw["data"] = dark
            
    return dark
        


def extract_darks_file_from_nx(args):        
    dark = 300 # default value
    
    labeled_regions, nregions = ndimage.label(  np.equal( 2, args.control_keys  ) )

    if nregions :
        if nregions > 1 :
            print(" WARNING: more than one dark measurement was found but I will merge them all into one unique dark ")
            
        with  h5py.File( args.nexus_file ,"r") as fr :
            all_darks = fr[f"/{args.entry_name}/instrument/detector/data"][  args.globals_indexes[labeled_regions > 0] ]
        
        if args.median_dark:
            dark = np.median(all_darks, axis=0)
        else:
            dark = np.mean(all_darks, axis=0)
            
        with h5py.File( os.path.join(args.target_scan_dir,"dark.h5"), "w" ) as fw:
            fw["data"] = dark
            
    return dark


        
def extract_flats_from_nx(args, dark,  unwrapped_angles_indexes , unwrapped_angles  ):
    labeled_regions, nregions = ndimage.label(  np.equal( 1, args.control_keys  ) )

    if nregions:

        flats = []
        flats_currents = []
        flats_angles_unwrapped = []
    
        for label in range( 1 , nregions+1):
            
            flat_angle = 0
            
            with  h5py.File( args.nexus_file ,"r") as fr :

                where_idx = list( args.globals_indexes[ labeled_regions == label ]) 
                
                all_flats = fr[args.nx_data_path][ where_idx  ]
                all_currents = fr[f"/{args.entry_name}/control/data"][ where_idx  ]

                # rescaling flats to nominal current
                all_flats = dark + (all_flats - dark ) * 0.2 / (all_currents[:,None,None])
                
                if args.median_flat:
                    flats.append( np.median(all_flats, axis=0))
                else:
                    flats.append( np.mean(all_flats, axis=0))

                flats_currents.append(0.2)
            
                region_start = args.globals_indexes[  labeled_regions == label    ].min()
                region_end   = 1 + args.globals_indexes[  labeled_regions == label    ].max()

                region_middle = 0.5*( region_start + region_end )

                my_unwrapped_angle = np.interp( region_middle,  unwrapped_angles_indexes , unwrapped_angles   )

                flats_angles_unwrapped.append(my_unwrapped_angle )


        with h5py.File( os.path.join(args.target_scan_dir,"flats.h5"), "w" ) as fw:
            fw["data"] = flats
            fw.create_group("framewise")
            fw["framewise/control"] = flats_currents
            fw["framewise/angles_unwrapped_deg"] = flats_angles_unwrapped

if __name__ == "__main__":
    main()
