import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Text, Environment, Float } from '@react-three/drei';
import * as THREE from 'three';

const CodeSymbol = () => {
  const groupRef = useRef();

  useFrame((state) => {
    groupRef.current.rotation.y = state.clock.elapsedTime * 0.2;
    groupRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.2;
  });

  return (
    <group ref={groupRef}>
      <Float speed={2} rotationIntensity={1} floatIntensity={1}>
        <Text
          fontSize={2}
          color="#64ffda"
          font="https://fonts.gstatic.com/s/roboto/v27/KFOmCnqEu92Fr1Mu4mxK.woff"
          anchorX="center"
          anchorY="middle"
          letterSpacing={0.1}
        >
          {`{ }`}
        </Text>
      </Float>
    </group>
  );
};

const CodeIcon3D = () => {
  return (
    <div style={{ height: '300px', width: '100%' }}>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.8} />
        <pointLight position={[10, 10, 10]} />
        <CodeSymbol />
        <Environment preset="sunset" />
      </Canvas>
    </div>
  );
};

export default CodeIcon3D;