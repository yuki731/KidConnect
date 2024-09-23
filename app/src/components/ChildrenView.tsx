import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchChildrenInFamily } from '../api/api';

const ChildrenList = () => {
    const [children, setChildren] = useState([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const token = localStorage.getItem('token');  // トークンをローカルストレージから取得
        if (token) {
            fetchChildrenInFamily(token)
                .then(data => setChildren(data))
                .catch(err => setError('Error fetching data'));
        }
    }, []);

    return (
        <div>
            {error ? <p>{error}</p> : null}
            <ul>
            {children.map((child: any) => (
                <li key={child.id}>
                <Link to={`/children_detail/${child.id}`}>{child.username}</Link>
                </li>
            ))}
            </ul>
        </div>
    );
};

export default ChildrenList;
