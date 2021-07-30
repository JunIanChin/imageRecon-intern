import open3d as o3d 

pcd = o3d.io.read_point_cloud("C:/Users/chin1/Desktop/final/final_meshed.ply")
o3d.visualization.draw_geometries([pcd])