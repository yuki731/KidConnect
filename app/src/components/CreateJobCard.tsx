import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createJobCard, fetchChildren } from '../api/api';  // API関数をインポート

interface Child {
  id: number;
  first_name: string;
}

const sampleImages = [
  { id: 1, src: '/images/sample1.png', alt: 'Sample Image 1' },
  { id: 2, src: '/images/sample2.png', alt: 'Sample Image 2' },
  { id: 3, src: '/images/sample3.png', alt: 'Sample Image 3' },
  { id: 4, src: '/images/sample4.png', alt: 'Sample Image 4' },
]; 

const CreateJobCardPage: React.FC = () => {
  const [children, setChildren] = useState<Child[]>([]);  // 子どものリストを保存する状態
  const [selectedChildren, setSelectedChildren] = useState<number[]>([]);  // 選択された子どものIDを保存する状態
  const [jobName, setJobName] = useState<string>('');  // お手伝いの名前
  const [money, setMoney] = useState<string>('');  // お手伝いの報酬
  const [jobImage, setJobImage] = useState<File | null>(null);  // お手伝いの画像
  const [selectedSampleImageId, setSelectedSampleImageId] = useState<number | null>(null);  // 選択されたサンプル画像のID
  const AuthToken = localStorage.getItem('token') || '';
  const [token, setToken] = useState<string>(AuthToken);  // 認証トークン
  const navigate = useNavigate();

  useEffect(() => {
    // 子どもリストを取得
    const fetchChildrenData = async () => {
      try {
        const data = await fetchChildren(token);
        setChildren(data);  // 取得した子どものリストを状態に保存
      } catch (error) {
        console.error('Error fetching children:', error);
      }
    };

    fetchChildrenData();
  }, []);

  const handleCheckboxChange = (childId: number) => {
    setSelectedChildren(prev =>
      prev.includes(childId) ? prev.filter(id => id !== childId) : [...prev, childId]
    );
  };

  const handleSampleImageSelect = async (imageSrc: string, imageId: number) => {
    try {
      const response = await fetch(imageSrc);
      const blob = await response.blob();
      const file = new File([blob], "sampleImage.png", { type: blob.type });

      setJobImage(file);  // サンプル画像をファイルとして設定
      setSelectedSampleImageId(imageId);  // 選択された画像のIDを設定
    } catch (error) {
      console.error('Error fetching the sample image:', error);
    }
  };

  const handleCustomImageSelect = (file: File | null) => {
    setJobImage(file);  // カスタム画像を選択
    setSelectedSampleImageId(null);  // サンプル画像の選択をクリア
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (selectedChildren.length === 0) {
      alert('少なくとも一人の子どもを選択してください。');
      return;
    }

    // FormDataを作成してAPI呼び出し
    const formData = new FormData();
    formData.append('job_name', jobName);
    formData.append('money', money.toString());
    if (jobImage) {
      formData.append('job_image', jobImage);  // 画像を追加
    }
    selectedChildren.forEach(childId => formData.append('child', childId.toString()));  // 子どものIDを追加

    try {
      const response = await createJobCard(token, formData);
      console.log('Job card created:', response);
      alert('お手伝いカードが作成されました！');
      navigate('/parents_dashboard');
    } catch (error) {
      console.error('Error creating job card:', error);
      alert('お手伝いカードの作成に失敗しました。');
    }
  };

  return (
    <div>
      <h1>お手伝いカードの作成</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>お手伝いの名前:</label>
          <input type="text" value={jobName} onChange={(e) => setJobName(e.target.value)} required />
        </div>
        <div>
          <label>報酬:</label>
          <input
            type="number"
            value={money}
            onChange={(e) => setMoney(e.target.value)}
          />
        </div>
        <div>
          <label>お手伝いの画像を選択するかアップロードしてください:</label>
          <div>
            {sampleImages.map((image) => (
              <div key={image.id} style={{ display: 'inline-block', margin: '10px' }}>
                <img
                  src={image.src}
                  alt={image.alt}
                  width="100"
                  height="100"
                  onClick={() => handleSampleImageSelect(image.src, image.id)}
                  style={{ cursor: 'pointer', border: selectedSampleImageId === image.id ? '2px solid red' : '2px solid transparent' }}
                />
              </div>
            ))}
          </div>
          <input
            type="file"
            onChange={(e) => handleCustomImageSelect(e.target.files ? e.target.files[0] : null)}
          />
        </div>
        <div>
          <h3>子どもを選択してください:</h3>
          {children.map((child) => (
            <div key={child.id}>
              <label>
                <input
                  type="checkbox"
                  value={child.id}
                  checked={selectedChildren.includes(child.id)}
                  onChange={() => handleCheckboxChange(child.id)}
                />
                {child.first_name}
              </label>
            </div>
          ))}
        </div>
        <button type="submit">お手伝いカードを作成</button>
      </form>
    </div>
  );
};

export default CreateJobCardPage;
