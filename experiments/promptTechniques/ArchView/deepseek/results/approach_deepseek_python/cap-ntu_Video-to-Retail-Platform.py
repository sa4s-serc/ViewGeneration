import graphviz

dot = graphviz.Digraph(comment='Hysia Video-to-Retail Platform Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_frontend') as c:
    c.attr(label='Frontend Layer', style='filled', color='lightblue')
    c.node('react_dashboard', 'React Dashboard\nMaterial-UI\nRedux State Management')
    c.node('user_management', 'User Management')
    c.node('model_management', 'Model Management')
    c.node('video_browsing', 'Video Browsing')
    c.node('resource_monitoring', 'Resource Monitoring')

with dot.subgraph(name='cluster_backend') as c:
    c.attr(label='Backend Layer', style='filled', color='lightgreen')
    c.node('django_backend', 'Django Backend\nRESTful & gRPC APIs')
    c.node('video_decoding', 'Video Decoding\nHysiaDecode\nCPUDecoder/GPUDecoder')
    c.node('multimodal_processing', 'Multimodal Processing\nVideo/Audio/Subtitles')
    c.node('system_monitoring', 'System Monitoring\nCPU/GPU/Memory/Network')
    c.node('data_handling', 'Data Handling\nSQLite/Pickle Indexing')

with dot.subgraph(name='cluster_ml') as c:
    c.attr(label='Machine Learning Layer', style='filled', color='orange')
    c.node('object_detection', 'Object Detection\nSSD/Faster R-CNN/MMdetection')
    c.node('face_recognition', 'Face Recognition\nTensorFlow/PyTorch')
    c.node('scene_recognition', 'Scene Recognition\nPlaces365/SoundNet')
    c.node('sentence_embedding', 'Sentence Embedding\nUniversal Sentence Encoder')
    c.node('model_serving', 'Model Serving\nClipper Integration')

with dot.subgraph(name='cluster_infrastructure') as c:
    c.attr(label='Infrastructure Layer', style='filled', color='lightyellow')
    c.node('gpu_acceleration', 'GPU Acceleration\nCUDA/FFmpeg')
    c.node('async_processing', 'Asynchronous Processing\nDecodeQueue')
    c.node('docker_deployment', 'Docker Deployment')
    c.node('performance_optimization', 'Performance Optimization\nCython/Quantization')

dot.edge('react_dashboard', 'django_backend', label='HTTP/gRPC')
dot.edge('django_backend', 'video_decoding', label='Video Input')
dot.edge('video_decoding', 'multimodal_processing', label='Decoded Data')
dot.edge('multimodal_processing', 'object_detection', label='Processed Frames')
dot.edge('multimodal_processing', 'face_recognition', label='Face Data')
dot.edge('multimodal_processing', 'scene_recognition', label='Scene/Audio Data')
dot.edge('multimodal_processing', 'sentence_embedding', label='Text Data')
dot.edge('object_detection', 'data_handling', label='Detection Results')
dot.edge('face_recognition', 'data_handling', label='Recognition Results')
dot.edge('scene_recognition', 'data_handling', label='Classification Results')
dot.edge('sentence_embedding', 'data_handling', label='Embedding Results')
dot.edge('data_handling', 'react_dashboard', label='Analysis Results')
dot.edge('system_monitoring', 'resource_monitoring', label='Metrics')
dot.edge('gpu_acceleration', 'video_decoding', label='GPU Processing')
dot.edge('gpu_acceleration', 'object_detection', label='Model Inference')
dot.edge('async_processing', 'video_decoding', label='Thread Management')
dot.edge('docker_deployment', 'django_backend', label='Containerization')
dot.edge('performance_optimization', 'video_decoding', label='Optimized Code')
dot.edge('performance_optimization', 'object_detection', label='Quantized Models')
dot.edge('model_serving', 'django_backend', label='Model Predictions')

dot.render('hysia_architecture', format='png', cleanup=True)