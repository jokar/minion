"""Test everything about packs reading and writing"""
from lib import (
					TestBase,
					with_rw_directory, 
					with_packs_rw,
					fixture_path
				)
from gitdb.stream import DeltaApplyReader

from gitdb.pack import (
							PackEntity,
							PackIndexFile,
							PackFile
						)

from gitdb.base import (
							OInfo, 
							OStream,
						)

from gitdb.fun import delta_types
from gitdb.exc import UnsupportedOperation
from gitdb.util import to_bin_sha
from itertools import izip
import os


#{ Utilities
def bin_sha_from_filename(filename):
	return to_bin_sha(os.path.splitext(os.path.basename(filename))[0][5:])
#} END utilities

class TestPack(TestBase):
	
	packindexfile_v1 = (fixture_path('packs/pack-c0438c19fb16422b6bbcce24387b3264416d485b.idx'), 1, 67)
	packindexfile_v2 = (fixture_path('packs/pack-11fdfa9e156ab73caae3b6da867192221f2089c2.idx'), 2, 30)
	packindexfile_v2_3_ascii = (fixture_path('packs/pack-a2bf8e71d8c18879e499335762dd95119d93d9f1.idx'), 2, 42)
	packfile_v2_1 = (fixture_path('packs/pack-c0438c19fb16422b6bbcce24387b3264416d485b.pack'), 2, packindexfile_v1[2])
	packfile_v2_2 = (fixture_path('packs/pack-11fdfa9e156ab73caae3b6da867192221f2089c2.pack'), 2, packindexfile_v2[2])
	packfile_v2_3_ascii = (fixture_path('packs/pack-a2bf8e71d8c18879e499335762dd95119d93d9f1.pack'), 2, packindexfile_v2_3_ascii[2])
	
	
	def _assert_index_file(self, index, version, size):
		assert index.packfile_checksum() != index.indexfile_checksum()
		assert len(index.packfile_checksum()) == 20
		assert len(index.indexfile_checksum()) == 20
		assert index.version() == version
		assert index.size() == size
		assert len(index.offsets()) == size
		
		# get all data of all objects
		for oidx in xrange(index.size()):
			sha = index.sha(oidx)
			assert oidx == index.sha_to_index(sha)
			
			entry = index.entry(oidx)
			assert len(entry) == 3
			
			assert entry[0] == index.offset(oidx)
			assert entry[1] == sha
			assert entry[2] == index.crc(oidx)
			
			# verify partial sha
			for l in (4,8,11,17,20):
				assert index.partial_sha_to_index(sha[:l], l*2) == oidx
			
		# END for each object index in indexfile
		self.failUnlessRaises(ValueError, index.partial_sha_to_index, "\0", 2)
		
		
	def _assert_pack_file(self, pack, version, size):
		assert pack.version() == 2
		assert pack.size() == size
		assert len(pack.checksum()) == 20
		
		num_obj = 0
		for obj in pack.stream_iter():
			num_obj += 1
			info = pack.info(obj.pack_offset)
			stream = pack.stream(obj.pack_offset)
			
			assert info.pack_offset == stream.pack_offset
			assert info.type_id == stream.type_id
			assert hasattr(stream, 'read')
			
			# it should be possible to read from both streams
			assert obj.read() == stream.read()
			
			streams = pack.collect_streams(obj.pack_offset)
			assert streams
			
			# read the stream
			try:
				dstream = DeltaApplyReader.new(streams)
			except ValueError:
				# ignore these, old git versions use only ref deltas, 
				# which we havent resolved ( as we are without an index )
				# Also ignore non-delta streams
				continue
			# END get deltastream
			
			# read all
			data = dstream.read()
			assert len(data) == dstream.size
			
			# test seek
			dstream.seek(0)
			assert dstream.read() == data
			
			
			# read chunks
			# NOTE: the current implementation is safe, it basically transfers
			# all calls to the underlying memory map
			
		# END for each object
		assert num_obj == size
		
	
	def test_pack_index(self):
		# check version 1 and 2
		for indexfile, version, size in (self.packindexfile_v1, self.packindexfile_v2): 
			index = PackIndexFile(indexfile)
			self._assert_index_file(index, version, size)
		# END run tests
		
	def test_pack(self):
		# there is this special version 3, but apparently its like 2 ... 
		for packfile, version, size in (self.packfile_v2_3_ascii, self.packfile_v2_1, self.packfile_v2_2):
			pack = PackFile(packfile)
			self._assert_pack_file(pack, version, size)
		# END for each pack to test
		
	def test_pack_entity(self):
		for packinfo, indexinfo in (	(self.packfile_v2_1, self.packindexfile_v1), 
										(self.packfile_v2_2, self.packindexfile_v2),
										(self.packfile_v2_3_ascii, self.packindexfile_v2_3_ascii)):
			packfile, version, size = packinfo
			indexfile, version, size = indexinfo
			entity = PackEntity(packfile)
			assert entity.pack().path() == packfile
			assert entity.index().path() == indexfile
			
			count = 0
			for info, stream in izip(entity.info_iter(), entity.stream_iter()):
				count += 1
				assert info.binsha == stream.binsha
				assert len(info.binsha) == 20
				assert info.type_id == stream.type_id
				assert info.size == stream.size
				
				# we return fully resolved items, which is implied by the sha centric access
				assert not info.type_id in delta_types
				
				# try all calls
				assert len(entity.collect_streams(info.binsha))
				oinfo = entity.info(info.binsha)
				assert isinstance(oinfo, OInfo)
				assert oinfo.binsha is not None
				ostream = entity.stream(info.binsha)
				assert isinstance(ostream, OStream)
				assert ostream.binsha is not None
				
				# verify the stream
				try:
					assert entity.is_valid_stream(info.binsha, use_crc=True)
				except UnsupportedOperation:
					pass
				# END ignore version issues
				assert entity.is_valid_stream(info.binsha, use_crc=False)
			# END for each info, stream tuple
			assert count == size
			
		 # END for each entity
		
	def test_pack_64(self):
		# TODO: hex-edit a pack helping us to verify that we can handle 64 byte offsets
		# of course without really needing such a huge pack 
		pass
