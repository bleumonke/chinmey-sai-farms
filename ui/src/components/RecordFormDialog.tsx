import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Stack,
  Box,
} from '@mui/material';

export interface RecordFormDialogProps {
  open: boolean;
  title: string;
  formData: Record<string, string>;
  fields: { name: string; label: string }[];
  onClose: () => void;
  onChange: (name: string, value: string) => void;
  onSubmit: () => void;
  submitLabel?: string;
  extraContent?: React.ReactNode;
}

const RecordFormDialog: React.FC<RecordFormDialogProps> = ({
  open,
  title,
  formData,
  fields,
  onClose,
  onChange,
  onSubmit,
  submitLabel = 'Submit',
  extraContent,
}) => {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="md"
      scroll="paper" // 👈 Enables scrollable paper content
      PaperProps={{
        sx: {
          backgroundColor: '#fff',
          color: '#000',
        },
      }}
    >
      <DialogTitle>{title}</DialogTitle>

      <DialogContent
        dividers
        sx={{
          maxHeight: '65vh', // 👈 Controls vertical scroll area
          px: 4,
          py: 2,
        }}
      >
        <Stack spacing={2}>
          {fields.map((field) => (
            <TextField
              key={field.name}
              label={field.label}
              value={formData[field.name] || ''}
              onChange={(e) => onChange(field.name, e.target.value)}
              fullWidth
              variant="outlined"
              sx={{
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: '#ccc',
                  },
                  '&:hover fieldset': {
                    borderColor: '#999',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#666',
                  },
                },
                input: {
                  color: '#000',
                },
                label: {
                  color: '#000',
                },
              }}
            />
          ))}
          {extraContent && <Box mt={2}>{extraContent}</Box>}
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={onSubmit} variant="contained">
          {submitLabel}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default RecordFormDialog;