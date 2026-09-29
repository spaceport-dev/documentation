import io,json,subprocess,sys,tarfile,tempfile,unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'fetch.py'
class FetchTests(unittest.TestCase):
 def test_fetch_and_failed_update_preserve_current_docs(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); archive=root/'docs.tar.gz'; destination=root/'documentation'; destination.mkdir()
   (destination/'README.md').write_text('Fetch instructions')
   with tarfile.open(archive,'w:gz') as tar:
    for name in ['_index.md','_toc.md','routing-api.md']:
     data=b'# Documentation\n'; info=tarfile.TarInfo('repo/documentation/'+name); info.size=len(data); tar.addfile(info,io.BytesIO(data))
   command=[sys.executable,str(SCRIPT),'--revision','a'*40,'--destination',str(destination),'--archive',str(archive)]
   result=subprocess.run(command,capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   self.assertEqual((destination/'README.md').read_text(),'Fetch instructions')
   self.assertTrue((destination/'routing-api.md').exists())
   self.assertEqual(json.loads((destination/'.spaceport-docs.json').read_text())['revision'],'a'*40)
   archive.write_bytes(b'broken download')
   result=subprocess.run(command,capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0)
   self.assertEqual((destination/'routing-api.md').read_text(),'# Documentation\n')
 def test_existing_unmanaged_files_are_not_overwritten(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/'routing-api.md').write_text('My edited doc')
   result=subprocess.run([sys.executable,str(SCRIPT),'--revision','a'*40,'--destination',str(root)],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0)
   self.assertIn('unmanaged',result.stderr.lower())
   self.assertEqual((root/'routing-api.md').read_text(),'My edited doc')
if __name__=='__main__': unittest.main()
