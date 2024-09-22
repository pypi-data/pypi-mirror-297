import h5py
import os
import numpy as np
import copy

class ETFFile:
    def __init__(self, etf_filename=None, etf_scan=None, slicing=slice(None,None,None)):
        if etf_filename is not None:
            self.init_from_file(etf_filename)
        elif etf_scan is not None:
            self.init_from_scan(etf_scan, slicing)
            
    def init_from_scan(self, etf_scan, slicing):

        assert (isinstance(etf_scan, ETFFile)), "the scan argument should be an ETFFile object"

        if slicing != slice(None,None,None):
            assert   (len(etf_scan.vsources_infos)==1) ,"When slicing a scan this must come from one source only"

            original_file_path, original_data_shape, original_slicing, original_data_dtype = etf_scan.vsources_infos[0]

            np_all, ny, nx =  original_data_shape            


            indices = list(range(np_all))[original_slicing][slicing]

            new_step = 1
            if len(indices) > 1:
                new_step = indices[1] - indices[0]
            
            new_slicing = slice(indices[0], indices[-1]+1, new_step )
            
            self.vsources_infos = [(original_file_path,  original_data_shape, new_slicing, original_data_dtype,   )]
        else:
            self.vsources_infos = copy.deepcopy(etf_scan.vsources_infos )

            
        self.globals={}
        for key in etf_scan.globals:
            self.globals[key] = etf_scan.globals[key]
            
        self.framewise={}
        for key in etf_scan.framewise:
            self.framewise[key] = etf_scan.framewise[key][slicing]


    @classmethod
    def join(cls, *args):
        etfscans = args

        new_scan = cls()
        
        new_scan.vsources_infos = []
        for scan in etfscans:
            new_scan.vsources_infos.extend(scan.vsources_infos)
            
        one_scan = args[0]
        
        new_scan.globals = {}

        for key in one_scan.globals:
            new_scan.globals[key] = one_scan.globals[key]
            if key != "bliss_original_files":
                for other_scan in args[1:]:
                    if new_scan.globals[key] != one_scan.globals[key]:
                        print(f" WARNING : while joining scan I encountered different values of key {key}")
            else:
                for other_scan in args[1:]:
                    new_scan.globals[key] = list(new_scan.globals[key]) + list( one_scan.globals[key])
                        
        new_scan.framewise = {}

        for key in one_scan.framewise:
            new_scan.framewise[key] = [one_scan.framewise[key]]
            for other_scan in args[1:]:
                new_scan.framewise[key].append( one_scan.framewise[key])
            new_scan.framewise[key] = np.concatenate(new_scan.framewise[key])

        return new_scan
            
    def init_from_file(self, etf_filename):
        with h5py.File( etf_filename ,"r") as fr:
            data_shape = fr["data"].shape
            data_dtype = fr["data"].dtype
            
            # h5py.VirtualSource(os.path.realpath(etf_filename), "data", data_shape  )
            self.vsources_infos = [(os.path.realpath(etf_filename),  data_shape, slice(None,None,None), data_dtype,   )]
            
            self.globals={}
            if "globals" in fr:
                for key in fr["globals"]:
                    self.globals[key] = fr["globals"][key][()]
                
            self.framewise={}
            if "framewise" in fr:
                for key in fr["framewise"]:
                    self.framewise[key] = fr["framewise"][key][()]

    def save(self, target_name, target_dir=None, ftype="projections"):
    
        target_dir = target_dir or os.path.realpath(os.curdir)
        target_name =  target_name + ".etf"

        target_scan_dir = os.path.join( target_dir, target_name )

        os.makedirs( target_scan_dir, exist_ok=True)

        target_file = os.path.join( target_scan_dir,  ftype +".h5"  )

        total_stack = 0
        for real_path, data_shape, slicing, data_dtype  in self.vsources_infos:
            np_all, ny, nx =  data_shape
            np = len(range( * slicing.indices(np_all) ) )
            total_stack += np

        new_layout = h5py.VirtualLayout(shape= (total_stack, ny, nx) , dtype= data_dtype)
                    
        total_stack = 0
        for real_path, data_shape, slicing, data_dtype  in self.vsources_infos:
            
            np_all, ny, nx =  data_shape
            
            np = len(range( * slicing.indices(np_all) ) )
            
            vsource =  h5py.VirtualSource(  os.path.relpath( real_path, target_scan_dir ), "data", data_shape  )
            
            new_layout[total_stack:total_stack + np] = vsource[slicing]
            
            total_stack += np
            
            
        with h5py.File( target_file, "w" ) as fw:
            fw.create_virtual_dataset("data", new_layout, fillvalue=0)

            fw.create_group("globals")
            for key in self.globals:
                fw["globals"][key] = self.globals[key]
            
            fw.create_group("framewise")
            for key in self.framewise:
                fw["framewise"][key] = self.framewise[key]
        
if __name__ == "__main__" :
    etffile = ETFFile(etf_filename="etftest/projections.h5")
    etffile.save("etftest_bis")

    new_scan = ETFFile.join(  ETFFile( etf_scan= etfscan , slicing =  slice(None, 1000)   )  , ETFFile( etf_scan=etfscan, slicing = slice(2000, None) )   )
    
    new_scan.save("newscan")
