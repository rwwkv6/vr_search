using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ForestGenerator : MonoBehaviour
{
    public Rigidbody tree;
    public Transform treePos;
    public ArrayList treeLocations = new ArrayList();
    public List<Vector3> xyz = new List<Vector3>();
    // Start is called before the first frame update
    void Start()
    {
        using (var reader = new StreamReader(@"C:/Users/rwwkv/Documents/treecoords.csv"))
        {
            while (!reader.EndOfStream)
            {
                var line = reader.ReadLine();
                var values = line.Split(',');
                var x = float.Parse(values[0]);
                var y = float.Parse(values[1]);
                var z = float.Parse(values[2]);
                treeLocations.Add(new Vector3(x,y,z));
            }
        }
        foreach (Vector3 xyz in treeLocations)
        {
            Vector3 coords = xyz;
            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cube.transform.position = xyz;
        }

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
