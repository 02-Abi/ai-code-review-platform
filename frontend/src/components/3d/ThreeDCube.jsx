import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Text, Box, OrbitControls, Environment } from '@react-three/drei';
import * as THREE from 'three';

const RotatingCube = () => {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta * 0.2;
    meshRef.current.rotation.y += delta * 0.3;
  });

  return (
    <mesh
      ref={meshRef}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      scale={hovered ? 1.2 : 1}
    >
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial
        color={hovered ? '#ff6b6b' : '#64ffda'}
        emissive={hovered ? '#ff6b6b' : '#64ffda'}
        emissiveIntensity={0.1}
        metalness={0.7}
        roughness={0.3}
        wireframe={false}
      />
    </mesh>
  );
};

const ThreeDCube = () => {
  return (
    <div style={{ height: '400px', width: '100%', position: 'relative' }}>
      <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Environment preset="city" />
        <RotatingCube />
        <OrbitControls enableZoom={true} enablePan={false} />
      </Canvas>
    </div>
  );
};

export default ThreeDCube;