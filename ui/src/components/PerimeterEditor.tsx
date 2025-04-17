import React from 'react';
import { Button, Stack, TextField } from '@mui/material';

type PerimeterCoordinates = { [key: string]: { lat: number; lng: number } };

interface PerimeterEditorProps {
  value: PerimeterCoordinates;
  onChange: (value: PerimeterCoordinates) => void;
}

const PerimeterEditor: React.FC<PerimeterEditorProps> = ({ value, onChange }) => {
  const handleAdd = () => {
    const key = `point_${Object.keys(value).length + 1}`;
    onChange({ ...value, [key]: { lat: 0, lng: 0 } });
  };

  const updateValue = (key: string, field: 'lat' | 'lng', fieldValue: number) => {
    onChange({
      ...value,
      [key]: { ...value[key], [field]: fieldValue }
    });
  };

  return (
    <Stack spacing={2}>
      <Button variant="outlined" onClick={handleAdd}>Add Perimeter Point</Button>
      {Object.entries(value).map(([key, coord]) => (
        <Stack direction="row" spacing={2} key={key}>
          <TextField
            label={`Lat (${key})`}
            type="number"
            value={coord.lat}
            onChange={(e) => updateValue(key, 'lat', parseFloat(e.target.value))}
          />
          <TextField
            label={`Lng (${key})`}
            type="number"
            value={coord.lng}
            onChange={(e) => updateValue(key, 'lng', parseFloat(e.target.value))}
          />
        </Stack>
      ))}
    </Stack>
  );
};

export default PerimeterEditor;
