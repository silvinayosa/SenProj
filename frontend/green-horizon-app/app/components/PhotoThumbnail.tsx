// components/PhotoThumbnail.tsx
import Image from 'next/image';

interface PhotoThumbnailProps {
  src: string;
  alt: string;
}

const PhotoThumbnail: React.FC<PhotoThumbnailProps> = ({ src, alt }) => {
  return (
    <div className="relative w-24 h-24 rounded-md overflow-hidden">
      <Image
        src={src}
        alt={alt}
        fill
        className="object-cover"
      />
    </div>
  );
};

export default PhotoThumbnail;