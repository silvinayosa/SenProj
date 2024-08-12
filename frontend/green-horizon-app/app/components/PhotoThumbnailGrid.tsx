// components/PhotoThumbnailGrid.tsx
import PhotoThumbnail from './PhotoThumbnail';

interface PhotoThumbnailGridProps {
  photos: { src: string; alt: string }[];
}

const PhotoThumbnailGrid: React.FC<PhotoThumbnailGridProps> = ({ photos }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {photos.map((photo, index) => (
        <PhotoThumbnail key={index} src={photo.src} alt={photo.alt} />
      ))}
    </div>
  );
};

export default PhotoThumbnailGrid;